import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..classes.StiComponent import StiComponent
from ..classes.StiEmailSettings import StiEmailSettings
from ..classes.StiHandler import StiHandler
from ..classes.StiResult import StiResult
from ..enums.StiComponentType import StiComponentType
from ..enums.StiEventType import StiEventType
from ..enums.StiHtmlMode import StiHtmlMode
from ..events.StiComponentEvent import StiComponentEvent
from ..events.StiReportEventArgs import StiReportEventArgs
from ..report.StiReport import StiReport
from .options.StiViewerOptions import StiViewerOptions


class StiViewer(StiComponent):

### Events
    
    onPrepareVariables: StiComponentEvent = None
    """The event is invoked before rendering a report after preparing report variables."""

    onBeginProcessData: StiComponentEvent = None
    """The event is invoked before data request, which needed to render a report."""

    onEndProcessData: StiComponentEvent = None
    """The event is invoked after loading data before rendering a report."""

    onOpenReport: StiComponentEvent = None
    """The event is invoked before opening a report from the viewer toolbar after clicking the button."""

    onOpenedReport: StiComponentEvent = None
    """The event is invoked after opening a report before showing."""

    onPrintReport: StiComponentEvent = None
    """The event is invoked before printing a report."""

    onBeginExportReport: StiComponentEvent = None
    """The event is invoked before exporting a report after the dialog of export settings."""

    onEndExportReport: StiComponentEvent = None
    """The event is invoked after exporting a report till its saving as a file."""

    onInteraction: StiComponentEvent = None
    """The event is invoked while interactive action of the viewer (dynamic sorting, collapsing, drill-down, applying of parameters)
    until processing values by the report generator."""

    onEmailReport: StiComponentEvent = None
    """The event is invoked after exporting a report before sending it by Email."""

    onDesignReport: StiComponentEvent = None
    """The event occurs when clicking on the Design button in the viewer toolbar."""
    

### Private

    __options: StiViewerOptions = None
    __report: StiReport = None


### Properties

    @property
    def componentType(self) -> str:
        return StiComponentType.VIEWER

    @property
    def handler(self) -> StiHandler:
        return super().handler
    
    @handler.setter
    def handler(self, value: StiHandler):
        super(type(self), type(self)).handler.fset(self, value)
        if value != None:
            value.component = self
            value.onBeginProcessData = self.onBeginProcessData
            value.onEndProcessData = self.onEndProcessData
            value.onPrepareVariables = self.onPrepareVariables

    @property
    def report(self) -> StiReport:
        return self.__report
    
    @report.setter
    def report(self, value: StiReport):
        self.__report = value
        if value != None:
            value.onBeginProcessData = self.onBeginProcessData
            value.onEndProcessData = self.onEndProcessData
            value.onPrepareVariables = self.onPrepareVariables
            value.handler = self.handler
            value.license = self.license
    
    @property
    def options(self) -> StiViewerOptions:
        """All options and settings of the viewer, divided by categories."""

        return self.__options
    
    @options.setter
    def options(self, value: StiViewerOptions):
        if value != None:
            value.component = self
            self.__options = value


### Private: Event handlers
    
    def __getOpenedReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        result = self._getDefaultEventResult(self.onOpenedReport, args)
        if result != None and args.report != self.handler.request.report:
            result.report = args.report

        return result

    def __getPrintReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        result = self._getDefaultEventResult(self.onPrintReport, args)
        if result != None and args.report != self.handler.request.report:
            result.report = args.report

        return result

    def __getBeginExportReportResult(self) -> StiResult:
        from ..events.StiExportEventArgs import StiExportEventArgs
        args = StiExportEventArgs(self.handler.request)
        result = self._getDefaultEventResult(self.onBeginExportReport, args)
        if result != None:
            if args.fileName != self.handler.request.fileName:
                result.fileName = args.fileName
            if args.settings != self.handler.request.settings:
                result.settings = args.settings
        
        return result
    
    def __getEndExportReportResult(self) -> StiResult:
        from ..events.StiExportEventArgs import StiExportEventArgs
        args = StiExportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onEndExportReport, args)
    
    """
    def __getInteractionResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onInteraction, args)
    """
    
    def __getEmailReportResult(self) -> StiResult:
        from ..events.StiEmailEventArgs import StiEmailEventArgs
        args = StiEmailEventArgs(self.handler.request)

        settings = StiEmailSettings()
        settings.toAddr = args.settings['email']
        settings.subject = args.settings['subject']
        settings.message = args.settings['message']
        settings.attachmentName = args.fileName if args.fileName.endswith('.' + args.fileExtension) else args.fileName + '.' + args.fileExtension

        args.settings = settings
        result = self._getDefaultEventResult(self.onEmailReport, args)
        if result == None or result.success == False:
            return result
            
        settings = args.settings

        part1 = MIMEText(settings.message, 'plain')
        part2 = MIMEBase('application', 'octet-stream')
        part2.set_payload(args.data)
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', f'attachment; filename={settings.attachmentName}')
        
        message = MIMEMultipart('alternative')
        message['Subject'] = settings.subject
        message['From'] = settings.fromAddr
        message['To'] = settings.toAddr
        message['Cc'] = ', '.join(settings.cc)
        message['Bcc'] = ', '.join(settings.bcc)
        message.attach(part1)
        message.attach(part2)
        text = message.as_string()
        
        try:
            if settings.secure.lower() == 'tls':
                server = smtplib.SMTP(settings.host, settings.port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(settings.host, settings.port)

            server.login(settings.login, settings.password)
            server.sendmail(settings.fromAddr, settings.toAddr, text)
            server.quit()

        except Exception as e:
            message = str(e)
            return StiResult.getError(message)

        return result
        

### Protected

    def _getComponentHtml(self) -> str:
        result = ''

        result += self.options.getHtml()
        result += f"let {self.id} = new Stimulsoft.Viewer.StiViewer({self.options.id}, '{self.id}', false);\n"

        result += self.onPrepareVariables.getHtml(True)
        result += self.onBeginProcessData.getHtml(True)
        result += self.onEndProcessData.getHtml()
        result += self.onOpenReport.getHtml()
        result += self.onOpenedReport.getHtml(True)
        result += self.onPrintReport.getHtml(True)
        result += self.onBeginExportReport.getHtml(True)
        result += self.onEndExportReport.getHtml(False, True)
        result += self.onInteraction.getHtml(True, False, False)
        result += self.onEmailReport.getHtml(True)
        result += self.onDesignReport.getHtml(False, False, False)

        if self.report != None:
            if not self.report.htmlRendered:
                result += self.report.getHtml(StiHtmlMode.SCRIPTS)

            result += f'{self.id}.report = {self.report.id};\n'

        result += f"{self.id}.renderHtml('{self.id}Content');\n"

        return result
    

### Public

    def getEventResult(self) -> StiResult:
        if self.request.event == StiEventType.OPENED_REPORT:
            return self.__getOpenedReportResult()
        
        if self.request.event == StiEventType.PRINT_REPORT:
            return self.__getPrintReportResult()

        if self.request.event == StiEventType.BEGIN_EXPORT_REPORT:
            return self.__getBeginExportReportResult()
        
        if self.request.event == StiEventType.END_EXPORT_REPORT:
            return self.__getEndExportReportResult()
        
        """
        if self.request.event == StiEventType.INTERACTION:
            return self.__getInteractionResult()
        """
        
        if self.request.event == StiEventType.EMAIL_REPORT:
            return self.__getEmailReportResult()
        
        return super().getEventResult()

    def getHtml(self, mode = StiHtmlMode.HTML_SCRIPTS) -> str:
        """Get the HTML representation of the component."""

        if mode == StiHtmlMode.HTML_PAGE:
            self.options.toolbar.showFullScreenButton = False
            self.options.appearance.fullScreenMode = True

        return super().getHtml(mode)


### Constructor

    def __init__(self):
        super().__init__()

        self.id = 'viewer'
        self.options = StiViewerOptions()

        self.onBeginProcessData = StiComponentEvent(self, 'onBeginProcessData')
        self.onBeginProcessData += True

        self.onEndProcessData = StiComponentEvent(self, 'onEndProcessData')
        self.onOpenReport = StiComponentEvent(self, 'onOpenReport')
        self.onOpenedReport = StiComponentEvent(self, 'onOpenedReport')
        self.onPrepareVariables = StiComponentEvent(self, 'onPrepareVariables')
        self.onPrintReport = StiComponentEvent(self, 'onPrintReport')
        self.onBeginExportReport = StiComponentEvent(self, 'onBeginExportReport')
        self.onEndExportReport = StiComponentEvent(self, 'onEndExportReport')
        self.onInteraction = StiComponentEvent(self, 'onInteraction')
        self.onEmailReport = StiComponentEvent(self, 'onEmailReport')
        self.onDesignReport = StiComponentEvent(self, 'onDesignReport')

        self.handler = StiHandler()
