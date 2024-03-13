# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore

from alibabacloud_gateway_spi.client import Client as SPIClient
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_gateway_dingtalk.client import Client as GatewayClientClient
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.card_1_0 import models as dingtalkcard__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    _client: SPIClient = None

    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._client = GatewayClientClient()
        self._spi = self._client
        self._endpoint_rule = ''
        if UtilClient.empty(self._endpoint):
            self._endpoint = 'api.dingtalk.com'

    def append_space_with_options(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceRequest,
        headers: dingtalkcard__1__0_models.AppendSpaceHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.AppendSpaceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AppendSpace',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/spaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.AppendSpaceResponse(),
            self.execute(params, req, runtime)
        )

    async def append_space_with_options_async(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceRequest,
        headers: dingtalkcard__1__0_models.AppendSpaceHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.AppendSpaceResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AppendSpace',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/spaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.AppendSpaceResponse(),
            await self.execute_async(params, req, runtime)
        )

    def append_space(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceRequest,
    ) -> dingtalkcard__1__0_models.AppendSpaceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.AppendSpaceHeaders()
        return self.append_space_with_options(request, headers, runtime)

    async def append_space_async(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceRequest,
    ) -> dingtalkcard__1__0_models.AppendSpaceResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.AppendSpaceHeaders()
        return await self.append_space_with_options_async(request, headers, runtime)

    def append_space_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceWithDelegateRequest,
        headers: dingtalkcard__1__0_models.AppendSpaceWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AppendSpaceWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/spaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def append_space_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceWithDelegateRequest,
        headers: dingtalkcard__1__0_models.AppendSpaceWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AppendSpaceWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/spaces',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def append_space_with_delegate(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.AppendSpaceWithDelegateHeaders()
        return self.append_space_with_delegate_with_options(request, headers, runtime)

    async def append_space_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.AppendSpaceWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.AppendSpaceWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.AppendSpaceWithDelegateHeaders()
        return await self.append_space_with_delegate_with_options_async(request, headers, runtime)

    def create_and_deliver_with_options(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverRequest,
        headers: dingtalkcard__1__0_models.CreateAndDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAndDeliver',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/createAndDeliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateAndDeliverResponse(),
            self.execute(params, req, runtime)
        )

    async def create_and_deliver_with_options_async(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverRequest,
        headers: dingtalkcard__1__0_models.CreateAndDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAndDeliver',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/createAndDeliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateAndDeliverResponse(),
            await self.execute_async(params, req, runtime)
        )

    def create_and_deliver(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverRequest,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateAndDeliverHeaders()
        return self.create_and_deliver_with_options(request, headers, runtime)

    async def create_and_deliver_async(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverRequest,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateAndDeliverHeaders()
        return await self.create_and_deliver_with_options_async(request, headers, runtime)

    def create_and_deliver_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateRequest,
        headers: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAndDeliverWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/createAndDeliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def create_and_deliver_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateRequest,
        headers: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateAndDeliverWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/createAndDeliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def create_and_deliver_with_delegate(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateAndDeliverWithDelegateHeaders()
        return self.create_and_deliver_with_delegate_with_options(request, headers, runtime)

    async def create_and_deliver_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.CreateAndDeliverWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.CreateAndDeliverWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateAndDeliverWithDelegateHeaders()
        return await self.create_and_deliver_with_delegate_with_options_async(request, headers, runtime)

    def create_card_with_options(
        self,
        request: dingtalkcard__1__0_models.CreateCardRequest,
        headers: dingtalkcard__1__0_models.CreateCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateCardResponse(),
            self.execute(params, req, runtime)
        )

    async def create_card_with_options_async(
        self,
        request: dingtalkcard__1__0_models.CreateCardRequest,
        headers: dingtalkcard__1__0_models.CreateCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateCardResponse(),
            await self.execute_async(params, req, runtime)
        )

    def create_card(
        self,
        request: dingtalkcard__1__0_models.CreateCardRequest,
    ) -> dingtalkcard__1__0_models.CreateCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateCardHeaders()
        return self.create_card_with_options(request, headers, runtime)

    async def create_card_async(
        self,
        request: dingtalkcard__1__0_models.CreateCardRequest,
    ) -> dingtalkcard__1__0_models.CreateCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateCardHeaders()
        return await self.create_card_with_options_async(request, headers, runtime)

    def create_card_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.CreateCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.CreateCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateCardWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def create_card_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.CreateCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.CreateCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.CreateCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_type):
            body['callbackType'] = request.callback_type
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_template_id):
            body['cardTemplateId'] = request.card_template_id
        if not UtilClient.is_unset(request.co_feed_open_space_model):
            body['coFeedOpenSpaceModel'] = request.co_feed_open_space_model
        if not UtilClient.is_unset(request.im_group_open_space_model):
            body['imGroupOpenSpaceModel'] = request.im_group_open_space_model
        if not UtilClient.is_unset(request.im_robot_open_space_model):
            body['imRobotOpenSpaceModel'] = request.im_robot_open_space_model
        if not UtilClient.is_unset(request.im_single_open_space_model):
            body['imSingleOpenSpaceModel'] = request.im_single_open_space_model
        if not UtilClient.is_unset(request.open_dynamic_data_config):
            body['openDynamicDataConfig'] = request.open_dynamic_data_config
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.top_open_space_model):
            body['topOpenSpaceModel'] = request.top_open_space_model
        if not UtilClient.is_unset(request.user_id):
            body['userId'] = request.user_id
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.CreateCardWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def create_card_with_delegate(
        self,
        request: dingtalkcard__1__0_models.CreateCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.CreateCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateCardWithDelegateHeaders()
        return self.create_card_with_delegate_with_options(request, headers, runtime)

    async def create_card_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.CreateCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.CreateCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.CreateCardWithDelegateHeaders()
        return await self.create_card_with_delegate_with_options_async(request, headers, runtime)

    def deliver_card_with_options(
        self,
        request: dingtalkcard__1__0_models.DeliverCardRequest,
        headers: dingtalkcard__1__0_models.DeliverCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.DeliverCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeliverCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/deliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.DeliverCardResponse(),
            self.execute(params, req, runtime)
        )

    async def deliver_card_with_options_async(
        self,
        request: dingtalkcard__1__0_models.DeliverCardRequest,
        headers: dingtalkcard__1__0_models.DeliverCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.DeliverCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeliverCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances/deliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.DeliverCardResponse(),
            await self.execute_async(params, req, runtime)
        )

    def deliver_card(
        self,
        request: dingtalkcard__1__0_models.DeliverCardRequest,
    ) -> dingtalkcard__1__0_models.DeliverCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.DeliverCardHeaders()
        return self.deliver_card_with_options(request, headers, runtime)

    async def deliver_card_async(
        self,
        request: dingtalkcard__1__0_models.DeliverCardRequest,
    ) -> dingtalkcard__1__0_models.DeliverCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.DeliverCardHeaders()
        return await self.deliver_card_with_options_async(request, headers, runtime)

    def deliver_card_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.DeliverCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.DeliverCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.DeliverCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeliverCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/deliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.DeliverCardWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def deliver_card_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.DeliverCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.DeliverCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.DeliverCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.co_feed_open_deliver_model):
            body['coFeedOpenDeliverModel'] = request.co_feed_open_deliver_model
        if not UtilClient.is_unset(request.doc_open_deliver_model):
            body['docOpenDeliverModel'] = request.doc_open_deliver_model
        if not UtilClient.is_unset(request.im_group_open_deliver_model):
            body['imGroupOpenDeliverModel'] = request.im_group_open_deliver_model
        if not UtilClient.is_unset(request.im_robot_open_deliver_model):
            body['imRobotOpenDeliverModel'] = request.im_robot_open_deliver_model
        if not UtilClient.is_unset(request.im_single_open_deliver_model):
            body['imSingleOpenDeliverModel'] = request.im_single_open_deliver_model
        if not UtilClient.is_unset(request.open_space_id):
            body['openSpaceId'] = request.open_space_id
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.top_open_deliver_model):
            body['topOpenDeliverModel'] = request.top_open_deliver_model
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeliverCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances/deliver',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.DeliverCardWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def deliver_card_with_delegate(
        self,
        request: dingtalkcard__1__0_models.DeliverCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.DeliverCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.DeliverCardWithDelegateHeaders()
        return self.deliver_card_with_delegate_with_options(request, headers, runtime)

    async def deliver_card_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.DeliverCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.DeliverCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.DeliverCardWithDelegateHeaders()
        return await self.deliver_card_with_delegate_with_options_async(request, headers, runtime)

    def register_callback_with_options(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackRequest,
        headers: dingtalkcard__1__0_models.RegisterCallbackHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.RegisterCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_secret):
            body['apiSecret'] = request.api_secret
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_url):
            body['callbackUrl'] = request.callback_url
        if not UtilClient.is_unset(request.force_update):
            body['forceUpdate'] = request.force_update
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RegisterCallback',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/callbacks/register',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.RegisterCallbackResponse(),
            self.execute(params, req, runtime)
        )

    async def register_callback_with_options_async(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackRequest,
        headers: dingtalkcard__1__0_models.RegisterCallbackHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.RegisterCallbackResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_secret):
            body['apiSecret'] = request.api_secret
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_url):
            body['callbackUrl'] = request.callback_url
        if not UtilClient.is_unset(request.force_update):
            body['forceUpdate'] = request.force_update
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RegisterCallback',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/callbacks/register',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.RegisterCallbackResponse(),
            await self.execute_async(params, req, runtime)
        )

    def register_callback(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackRequest,
    ) -> dingtalkcard__1__0_models.RegisterCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.RegisterCallbackHeaders()
        return self.register_callback_with_options(request, headers, runtime)

    async def register_callback_async(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackRequest,
    ) -> dingtalkcard__1__0_models.RegisterCallbackResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.RegisterCallbackHeaders()
        return await self.register_callback_with_options_async(request, headers, runtime)

    def register_callback_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackWithDelegateRequest,
        headers: dingtalkcard__1__0_models.RegisterCallbackWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_secret):
            body['apiSecret'] = request.api_secret
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_url):
            body['callbackUrl'] = request.callback_url
        if not UtilClient.is_unset(request.force_update):
            body['forceUpdate'] = request.force_update
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RegisterCallbackWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/callbacks/register',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def register_callback_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackWithDelegateRequest,
        headers: dingtalkcard__1__0_models.RegisterCallbackWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.api_secret):
            body['apiSecret'] = request.api_secret
        if not UtilClient.is_unset(request.callback_route_key):
            body['callbackRouteKey'] = request.callback_route_key
        if not UtilClient.is_unset(request.callback_url):
            body['callbackUrl'] = request.callback_url
        if not UtilClient.is_unset(request.force_update):
            body['forceUpdate'] = request.force_update
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RegisterCallbackWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/callbacks/register',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def register_callback_with_delegate(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.RegisterCallbackWithDelegateHeaders()
        return self.register_callback_with_delegate_with_options(request, headers, runtime)

    async def register_callback_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.RegisterCallbackWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.RegisterCallbackWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.RegisterCallbackWithDelegateHeaders()
        return await self.register_callback_with_delegate_with_options_async(request, headers, runtime)

    def streaming_update_with_options(
        self,
        request: dingtalkcard__1__0_models.StreamingUpdateRequest,
        headers: dingtalkcard__1__0_models.StreamingUpdateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.StreamingUpdateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.guid):
            body['guid'] = request.guid
        if not UtilClient.is_unset(request.is_error):
            body['isError'] = request.is_error
        if not UtilClient.is_unset(request.is_finalize):
            body['isFinalize'] = request.is_finalize
        if not UtilClient.is_unset(request.is_full):
            body['isFull'] = request.is_full
        if not UtilClient.is_unset(request.key):
            body['key'] = request.key
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='StreamingUpdate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/streaming',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.StreamingUpdateResponse(),
            self.execute(params, req, runtime)
        )

    async def streaming_update_with_options_async(
        self,
        request: dingtalkcard__1__0_models.StreamingUpdateRequest,
        headers: dingtalkcard__1__0_models.StreamingUpdateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.StreamingUpdateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.guid):
            body['guid'] = request.guid
        if not UtilClient.is_unset(request.is_error):
            body['isError'] = request.is_error
        if not UtilClient.is_unset(request.is_finalize):
            body['isFinalize'] = request.is_finalize
        if not UtilClient.is_unset(request.is_full):
            body['isFull'] = request.is_full
        if not UtilClient.is_unset(request.key):
            body['key'] = request.key
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='StreamingUpdate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/streaming',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.StreamingUpdateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def streaming_update(
        self,
        request: dingtalkcard__1__0_models.StreamingUpdateRequest,
    ) -> dingtalkcard__1__0_models.StreamingUpdateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.StreamingUpdateHeaders()
        return self.streaming_update_with_options(request, headers, runtime)

    async def streaming_update_async(
        self,
        request: dingtalkcard__1__0_models.StreamingUpdateRequest,
    ) -> dingtalkcard__1__0_models.StreamingUpdateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.StreamingUpdateHeaders()
        return await self.streaming_update_with_options_async(request, headers, runtime)

    def update_card_with_options(
        self,
        request: dingtalkcard__1__0_models.UpdateCardRequest,
        headers: dingtalkcard__1__0_models.UpdateCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.UpdateCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_update_options):
            body['cardUpdateOptions'] = request.card_update_options
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.UpdateCardResponse(),
            self.execute(params, req, runtime)
        )

    async def update_card_with_options_async(
        self,
        request: dingtalkcard__1__0_models.UpdateCardRequest,
        headers: dingtalkcard__1__0_models.UpdateCardHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.UpdateCardResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_update_options):
            body['cardUpdateOptions'] = request.card_update_options
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateCard',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/instances',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.UpdateCardResponse(),
            await self.execute_async(params, req, runtime)
        )

    def update_card(
        self,
        request: dingtalkcard__1__0_models.UpdateCardRequest,
    ) -> dingtalkcard__1__0_models.UpdateCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.UpdateCardHeaders()
        return self.update_card_with_options(request, headers, runtime)

    async def update_card_async(
        self,
        request: dingtalkcard__1__0_models.UpdateCardRequest,
    ) -> dingtalkcard__1__0_models.UpdateCardResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.UpdateCardHeaders()
        return await self.update_card_with_options_async(request, headers, runtime)

    def update_card_with_delegate_with_options(
        self,
        request: dingtalkcard__1__0_models.UpdateCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.UpdateCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.UpdateCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_update_options):
            body['cardUpdateOptions'] = request.card_update_options
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.UpdateCardWithDelegateResponse(),
            self.execute(params, req, runtime)
        )

    async def update_card_with_delegate_with_options_async(
        self,
        request: dingtalkcard__1__0_models.UpdateCardWithDelegateRequest,
        headers: dingtalkcard__1__0_models.UpdateCardWithDelegateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkcard__1__0_models.UpdateCardWithDelegateResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.card_data):
            body['cardData'] = request.card_data
        if not UtilClient.is_unset(request.card_update_options):
            body['cardUpdateOptions'] = request.card_update_options
        if not UtilClient.is_unset(request.out_track_id):
            body['outTrackId'] = request.out_track_id
        if not UtilClient.is_unset(request.private_data):
            body['privateData'] = request.private_data
        if not UtilClient.is_unset(request.user_id_type):
            body['userIdType'] = request.user_id_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateCardWithDelegate',
            version='card_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/card/me/instances',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkcard__1__0_models.UpdateCardWithDelegateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def update_card_with_delegate(
        self,
        request: dingtalkcard__1__0_models.UpdateCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.UpdateCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.UpdateCardWithDelegateHeaders()
        return self.update_card_with_delegate_with_options(request, headers, runtime)

    async def update_card_with_delegate_async(
        self,
        request: dingtalkcard__1__0_models.UpdateCardWithDelegateRequest,
    ) -> dingtalkcard__1__0_models.UpdateCardWithDelegateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkcard__1__0_models.UpdateCardWithDelegateHeaders()
        return await self.update_card_with_delegate_with_options_async(request, headers, runtime)
