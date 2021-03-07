from tethys_sdk.base import TethysAppBase, url_map_maker


class Streamflowhkh(TethysAppBase):
    """
    Tethys app class for Streamflowhkh.
    """

    name = 'ECMWF Streamflow Prediction Tool - Regional'
    index = 'streamflowhkh:home'
    icon = 'streamflowhkh/images/icon.gif'
    package = 'streamflowhkh'
    root_url = 'streamflowhkh'
    color = '#16a085'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []


    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)
        url_maps = (
            UrlMap(
                name='home',
                url='streamflowhkh',
                controller='streamflowhkh.controllers.index'),
            UrlMap(
                name='chart',
                url='streamflowhkh/chart',
                controller='streamflowhkh.controllers.chart'),
            UrlMap(
                name='forecastpercent',
                url='streamflowhkh/forecastpercent',
                controller='streamflowhkh.controllers.forecastpercent'),
            UrlMap(
                name='getFeatures',
                url='streamflowhkh/api/getFeatures',
                controller='streamflowhkh.api.getFeatures'),
            UrlMap(
                name='getreturnPeriod',
                url='streamflowhkh/api/getreturnPeriod',
                controller='streamflowhkh.api.getreturnPeriod'),
            UrlMap(
                name='getHistoric',
                url='streamflowhkh/api/getHistoric',
                controller='streamflowhkh.api.getHistoric'),
            UrlMap(
                name='getFlowDurationCurve',
                url='streamflowhkh/api/getFlowDurationCurve',
                controller='streamflowhkh.api.getFlowDurationCurve'),
            UrlMap(
                name='getForecast',
                url='streamflowhkh/api/getForecast',
                controller='streamflowhkh.api.getForecast'),
            UrlMap(
                name='getForecastCSV',
                url='streamflowhkh/getForecastCSV',
                controller='streamflowhkh.controllers.getForecastCSV'),
            UrlMap(
                name='getHistoricCSV',
                url='streamflowhkh/getHistoricCSV',
                controller='streamflowhkh.controllers.getHistoricCSV'),
        )
        return url_maps