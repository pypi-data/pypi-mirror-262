# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore

from alibabacloud_gateway_spi.client import Client as SPIClient
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_gateway_dingtalk.client import Client as GatewayClientClient
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.ats_1_0 import models as dingtalkats__1__0_models
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

    def add_application_reg_form_template_with_options(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
        headers: dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.name):
            body['name'] = request.name
        if not UtilClient.is_unset(request.outer_id):
            body['outerId'] = request.outer_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddApplicationRegFormTemplate',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/applicationRegForms/templates',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse(),
            self.execute(params, req, runtime)
        )

    async def add_application_reg_form_template_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
        headers: dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.name):
            body['name'] = request.name
        if not UtilClient.is_unset(request.outer_id):
            body['outerId'] = request.outer_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddApplicationRegFormTemplate',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/applicationRegForms/templates',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse(),
            await self.execute_async(params, req, runtime)
        )

    def add_application_reg_form_template(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders()
        return self.add_application_reg_form_template_with_options(request, headers, runtime)

    async def add_application_reg_form_template_async(
        self,
        request: dingtalkats__1__0_models.AddApplicationRegFormTemplateRequest,
    ) -> dingtalkats__1__0_models.AddApplicationRegFormTemplateResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddApplicationRegFormTemplateHeaders()
        return await self.add_application_reg_form_template_with_options_async(request, headers, runtime)

    def add_file_with_options(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
        headers: dingtalkats__1__0_models.AddFileHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.file_name):
            body['fileName'] = request.file_name
        if not UtilClient.is_unset(request.media_id):
            body['mediaId'] = request.media_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddFile',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/files',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddFileResponse(),
            self.execute(params, req, runtime)
        )

    async def add_file_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
        headers: dingtalkats__1__0_models.AddFileHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.file_name):
            body['fileName'] = request.file_name
        if not UtilClient.is_unset(request.media_id):
            body['mediaId'] = request.media_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddFile',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/files',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddFileResponse(),
            await self.execute_async(params, req, runtime)
        )

    def add_file(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddFileHeaders()
        return self.add_file_with_options(request, headers, runtime)

    async def add_file_async(
        self,
        request: dingtalkats__1__0_models.AddFileRequest,
    ) -> dingtalkats__1__0_models.AddFileResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddFileHeaders()
        return await self.add_file_with_options_async(request, headers, runtime)

    def add_user_account_with_options(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
        headers: dingtalkats__1__0_models.AddUserAccountHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        body = {}
        if not UtilClient.is_unset(request.channel_account_name):
            body['channelAccountName'] = request.channel_account_name
        if not UtilClient.is_unset(request.channel_user_identify):
            body['channelUserIdentify'] = request.channel_user_identify
        if not UtilClient.is_unset(request.phone_number):
            body['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddUserAccount',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/users/accounts',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddUserAccountResponse(),
            self.execute(params, req, runtime)
        )

    async def add_user_account_with_options_async(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
        headers: dingtalkats__1__0_models.AddUserAccountHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.corp_id):
            query['corpId'] = request.corp_id
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        body = {}
        if not UtilClient.is_unset(request.channel_account_name):
            body['channelAccountName'] = request.channel_account_name
        if not UtilClient.is_unset(request.channel_user_identify):
            body['channelUserIdentify'] = request.channel_user_identify
        if not UtilClient.is_unset(request.phone_number):
            body['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddUserAccount',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/users/accounts',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.AddUserAccountResponse(),
            await self.execute_async(params, req, runtime)
        )

    def add_user_account(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddUserAccountHeaders()
        return self.add_user_account_with_options(request, headers, runtime)

    async def add_user_account_async(
        self,
        request: dingtalkats__1__0_models.AddUserAccountRequest,
    ) -> dingtalkats__1__0_models.AddUserAccountResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.AddUserAccountHeaders()
        return await self.add_user_account_with_options_async(request, headers, runtime)

    def collect_recruit_job_detail_with_options(
        self,
        request: dingtalkats__1__0_models.CollectRecruitJobDetailRequest,
        headers: dingtalkats__1__0_models.CollectRecruitJobDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectRecruitJobDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.job_info):
            body['jobInfo'] = request.job_info
        if not UtilClient.is_unset(request.out_corp_id):
            body['outCorpId'] = request.out_corp_id
        if not UtilClient.is_unset(request.out_corp_name):
            body['outCorpName'] = request.out_corp_name
        if not UtilClient.is_unset(request.recruit_user_info):
            body['recruitUserInfo'] = request.recruit_user_info
        if not UtilClient.is_unset(request.source):
            body['source'] = request.source
        if not UtilClient.is_unset(request.update_time):
            body['updateTime'] = request.update_time
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectRecruitJobDetail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/jobs/import',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectRecruitJobDetailResponse(),
            self.execute(params, req, runtime)
        )

    async def collect_recruit_job_detail_with_options_async(
        self,
        request: dingtalkats__1__0_models.CollectRecruitJobDetailRequest,
        headers: dingtalkats__1__0_models.CollectRecruitJobDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectRecruitJobDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.job_info):
            body['jobInfo'] = request.job_info
        if not UtilClient.is_unset(request.out_corp_id):
            body['outCorpId'] = request.out_corp_id
        if not UtilClient.is_unset(request.out_corp_name):
            body['outCorpName'] = request.out_corp_name
        if not UtilClient.is_unset(request.recruit_user_info):
            body['recruitUserInfo'] = request.recruit_user_info
        if not UtilClient.is_unset(request.source):
            body['source'] = request.source
        if not UtilClient.is_unset(request.update_time):
            body['updateTime'] = request.update_time
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectRecruitJobDetail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/jobs/import',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectRecruitJobDetailResponse(),
            await self.execute_async(params, req, runtime)
        )

    def collect_recruit_job_detail(
        self,
        request: dingtalkats__1__0_models.CollectRecruitJobDetailRequest,
    ) -> dingtalkats__1__0_models.CollectRecruitJobDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectRecruitJobDetailHeaders()
        return self.collect_recruit_job_detail_with_options(request, headers, runtime)

    async def collect_recruit_job_detail_async(
        self,
        request: dingtalkats__1__0_models.CollectRecruitJobDetailRequest,
    ) -> dingtalkats__1__0_models.CollectRecruitJobDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectRecruitJobDetailHeaders()
        return await self.collect_recruit_job_detail_with_options_async(request, headers, runtime)

    def collect_resume_detail_with_options(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
        headers: dingtalkats__1__0_models.CollectResumeDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_code):
            body['channelCode'] = request.channel_code
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.channel_talent_id):
            body['channelTalentId'] = request.channel_talent_id
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.resume_channel_url):
            body['resumeChannelUrl'] = request.resume_channel_url
        if not UtilClient.is_unset(request.resume_data):
            body['resumeData'] = request.resume_data
        if not UtilClient.is_unset(request.resume_file):
            body['resumeFile'] = request.resume_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectResumeDetail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/resumes/details',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeDetailResponse(),
            self.execute(params, req, runtime)
        )

    async def collect_resume_detail_with_options_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
        headers: dingtalkats__1__0_models.CollectResumeDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_code):
            body['channelCode'] = request.channel_code
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.channel_talent_id):
            body['channelTalentId'] = request.channel_talent_id
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.resume_channel_url):
            body['resumeChannelUrl'] = request.resume_channel_url
        if not UtilClient.is_unset(request.resume_data):
            body['resumeData'] = request.resume_data
        if not UtilClient.is_unset(request.resume_file):
            body['resumeFile'] = request.resume_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectResumeDetail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/resumes/details',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeDetailResponse(),
            await self.execute_async(params, req, runtime)
        )

    def collect_resume_detail(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeDetailHeaders()
        return self.collect_resume_detail_with_options(request, headers, runtime)

    async def collect_resume_detail_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeDetailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeDetailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeDetailHeaders()
        return await self.collect_resume_detail_with_options_async(request, headers, runtime)

    def collect_resume_mail_with_options(
        self,
        request: dingtalkats__1__0_models.CollectResumeMailRequest,
        headers: dingtalkats__1__0_models.CollectResumeMailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeMailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_code):
            body['channelCode'] = request.channel_code
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.from_mail_address):
            body['fromMailAddress'] = request.from_mail_address
        if not UtilClient.is_unset(request.history_mail_import):
            body['historyMailImport'] = request.history_mail_import
        if not UtilClient.is_unset(request.mail_id):
            body['mailId'] = request.mail_id
        if not UtilClient.is_unset(request.mail_title):
            body['mailTitle'] = request.mail_title
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.receive_mail_address):
            body['receiveMailAddress'] = request.receive_mail_address
        if not UtilClient.is_unset(request.receive_mail_type):
            body['receiveMailType'] = request.receive_mail_type
        if not UtilClient.is_unset(request.received_time):
            body['receivedTime'] = request.received_time
        if not UtilClient.is_unset(request.resume_channel_url):
            body['resumeChannelUrl'] = request.resume_channel_url
        if not UtilClient.is_unset(request.resume_file):
            body['resumeFile'] = request.resume_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectResumeMail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/resumes/mails',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeMailResponse(),
            self.execute(params, req, runtime)
        )

    async def collect_resume_mail_with_options_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeMailRequest,
        headers: dingtalkats__1__0_models.CollectResumeMailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.CollectResumeMailResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel_code):
            body['channelCode'] = request.channel_code
        if not UtilClient.is_unset(request.deliver_job_id):
            body['deliverJobId'] = request.deliver_job_id
        if not UtilClient.is_unset(request.from_mail_address):
            body['fromMailAddress'] = request.from_mail_address
        if not UtilClient.is_unset(request.history_mail_import):
            body['historyMailImport'] = request.history_mail_import
        if not UtilClient.is_unset(request.mail_id):
            body['mailId'] = request.mail_id
        if not UtilClient.is_unset(request.mail_title):
            body['mailTitle'] = request.mail_title
        if not UtilClient.is_unset(request.opt_user_id):
            body['optUserId'] = request.opt_user_id
        if not UtilClient.is_unset(request.receive_mail_address):
            body['receiveMailAddress'] = request.receive_mail_address
        if not UtilClient.is_unset(request.receive_mail_type):
            body['receiveMailType'] = request.receive_mail_type
        if not UtilClient.is_unset(request.received_time):
            body['receivedTime'] = request.received_time
        if not UtilClient.is_unset(request.resume_channel_url):
            body['resumeChannelUrl'] = request.resume_channel_url
        if not UtilClient.is_unset(request.resume_file):
            body['resumeFile'] = request.resume_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CollectResumeMail',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/resumes/mails',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.CollectResumeMailResponse(),
            await self.execute_async(params, req, runtime)
        )

    def collect_resume_mail(
        self,
        request: dingtalkats__1__0_models.CollectResumeMailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeMailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeMailHeaders()
        return self.collect_resume_mail_with_options(request, headers, runtime)

    async def collect_resume_mail_async(
        self,
        request: dingtalkats__1__0_models.CollectResumeMailRequest,
    ) -> dingtalkats__1__0_models.CollectResumeMailResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.CollectResumeMailHeaders()
        return await self.collect_resume_mail_with_options_async(request, headers, runtime)

    def confirm_rights_with_options(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
        headers: dingtalkats__1__0_models.ConfirmRightsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ConfirmRights',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/rights/{rights_code}/confirm',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ConfirmRightsResponse(),
            self.execute(params, req, runtime)
        )

    async def confirm_rights_with_options_async(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
        headers: dingtalkats__1__0_models.ConfirmRightsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ConfirmRights',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/rights/{rights_code}/confirm',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ConfirmRightsResponse(),
            await self.execute_async(params, req, runtime)
        )

    def confirm_rights(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ConfirmRightsHeaders()
        return self.confirm_rights_with_options(rights_code, request, headers, runtime)

    async def confirm_rights_async(
        self,
        rights_code: str,
        request: dingtalkats__1__0_models.ConfirmRightsRequest,
    ) -> dingtalkats__1__0_models.ConfirmRightsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ConfirmRightsHeaders()
        return await self.confirm_rights_with_options_async(rights_code, request, headers, runtime)

    def finish_beginner_task_with_options(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
        headers: dingtalkats__1__0_models.FinishBeginnerTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.scope):
            query['scope'] = request.scope
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FinishBeginnerTask',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/beginnerTasks/{task_code}/finish',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.FinishBeginnerTaskResponse(),
            self.execute(params, req, runtime)
        )

    async def finish_beginner_task_with_options_async(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
        headers: dingtalkats__1__0_models.FinishBeginnerTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.scope):
            query['scope'] = request.scope
        if not UtilClient.is_unset(request.user_id):
            query['userId'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FinishBeginnerTask',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/beginnerTasks/{task_code}/finish',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.FinishBeginnerTaskResponse(),
            await self.execute_async(params, req, runtime)
        )

    def finish_beginner_task(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.FinishBeginnerTaskHeaders()
        return self.finish_beginner_task_with_options(task_code, request, headers, runtime)

    async def finish_beginner_task_async(
        self,
        task_code: str,
        request: dingtalkats__1__0_models.FinishBeginnerTaskRequest,
    ) -> dingtalkats__1__0_models.FinishBeginnerTaskResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.FinishBeginnerTaskHeaders()
        return await self.finish_beginner_task_with_options_async(task_code, request, headers, runtime)

    def get_application_reg_form_by_flow_id_with_options(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
        headers: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetApplicationRegFormByFlowId',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/{flow_id}/applicationRegForms',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse(),
            self.execute(params, req, runtime)
        )

    async def get_application_reg_form_by_flow_id_with_options_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
        headers: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetApplicationRegFormByFlowId',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/{flow_id}/applicationRegForms',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_application_reg_form_by_flow_id(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders()
        return self.get_application_reg_form_by_flow_id_with_options(flow_id, request, headers, runtime)

    async def get_application_reg_form_by_flow_id_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.GetApplicationRegFormByFlowIdRequest,
    ) -> dingtalkats__1__0_models.GetApplicationRegFormByFlowIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetApplicationRegFormByFlowIdHeaders()
        return await self.get_application_reg_form_by_flow_id_with_options_async(flow_id, request, headers, runtime)

    def get_candidate_by_phone_number_with_options(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
        headers: dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.phone_number):
            query['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCandidateByPhoneNumber',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/candidates',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse(),
            self.execute(params, req, runtime)
        )

    async def get_candidate_by_phone_number_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
        headers: dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.phone_number):
            query['phoneNumber'] = request.phone_number
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetCandidateByPhoneNumber',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/candidates',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_candidate_by_phone_number(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders()
        return self.get_candidate_by_phone_number_with_options(request, headers, runtime)

    async def get_candidate_by_phone_number_async(
        self,
        request: dingtalkats__1__0_models.GetCandidateByPhoneNumberRequest,
    ) -> dingtalkats__1__0_models.GetCandidateByPhoneNumberResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetCandidateByPhoneNumberHeaders()
        return await self.get_candidate_by_phone_number_with_options_async(request, headers, runtime)

    def get_file_upload_info_with_options(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
        headers: dingtalkats__1__0_models.GetFileUploadInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.file_name):
            query['fileName'] = request.file_name
        if not UtilClient.is_unset(request.file_size):
            query['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.md_5):
            query['md5'] = request.md_5
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetFileUploadInfo',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/files/uploadInfos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFileUploadInfoResponse(),
            self.execute(params, req, runtime)
        )

    async def get_file_upload_info_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
        headers: dingtalkats__1__0_models.GetFileUploadInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.file_name):
            query['fileName'] = request.file_name
        if not UtilClient.is_unset(request.file_size):
            query['fileSize'] = request.file_size
        if not UtilClient.is_unset(request.md_5):
            query['md5'] = request.md_5
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetFileUploadInfo',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/files/uploadInfos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFileUploadInfoResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_file_upload_info(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFileUploadInfoHeaders()
        return self.get_file_upload_info_with_options(request, headers, runtime)

    async def get_file_upload_info_async(
        self,
        request: dingtalkats__1__0_models.GetFileUploadInfoRequest,
    ) -> dingtalkats__1__0_models.GetFileUploadInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFileUploadInfoHeaders()
        return await self.get_file_upload_info_with_options_async(request, headers, runtime)

    def get_flow_id_by_relation_entity_id_with_options(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
        headers: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.relation_entity):
            query['relationEntity'] = request.relation_entity
        if not UtilClient.is_unset(request.relation_entity_id):
            query['relationEntityId'] = request.relation_entity_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetFlowIdByRelationEntityId',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/ids',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse(),
            self.execute(params, req, runtime)
        )

    async def get_flow_id_by_relation_entity_id_with_options_async(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
        headers: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.relation_entity):
            query['relationEntity'] = request.relation_entity
        if not UtilClient.is_unset(request.relation_entity_id):
            query['relationEntityId'] = request.relation_entity_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetFlowIdByRelationEntityId',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/ids',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_flow_id_by_relation_entity_id(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders()
        return self.get_flow_id_by_relation_entity_id_with_options(request, headers, runtime)

    async def get_flow_id_by_relation_entity_id_async(
        self,
        request: dingtalkats__1__0_models.GetFlowIdByRelationEntityIdRequest,
    ) -> dingtalkats__1__0_models.GetFlowIdByRelationEntityIdResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetFlowIdByRelationEntityIdHeaders()
        return await self.get_flow_id_by_relation_entity_id_with_options_async(request, headers, runtime)

    def get_job_auth_with_options(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
        headers: dingtalkats__1__0_models.GetJobAuthHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobAuth',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/auths/jobs/{job_id}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetJobAuthResponse(),
            self.execute(params, req, runtime)
        )

    async def get_job_auth_with_options_async(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
        headers: dingtalkats__1__0_models.GetJobAuthHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetJobAuth',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/auths/jobs/{job_id}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.GetJobAuthResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_job_auth(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetJobAuthHeaders()
        return self.get_job_auth_with_options(job_id, request, headers, runtime)

    async def get_job_auth_async(
        self,
        job_id: str,
        request: dingtalkats__1__0_models.GetJobAuthRequest,
    ) -> dingtalkats__1__0_models.GetJobAuthResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.GetJobAuthHeaders()
        return await self.get_job_auth_with_options_async(job_id, request, headers, runtime)

    def query_candidates_with_options(
        self,
        request: dingtalkats__1__0_models.QueryCandidatesRequest,
        headers: dingtalkats__1__0_models.QueryCandidatesHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryCandidatesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.max_results):
            body['maxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.stat_id):
            body['statId'] = request.stat_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='QueryCandidates',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/candidates/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryCandidatesResponse(),
            self.execute(params, req, runtime)
        )

    async def query_candidates_with_options_async(
        self,
        request: dingtalkats__1__0_models.QueryCandidatesRequest,
        headers: dingtalkats__1__0_models.QueryCandidatesHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryCandidatesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.op_user_id):
            query['opUserId'] = request.op_user_id
        body = {}
        if not UtilClient.is_unset(request.max_results):
            body['maxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.stat_id):
            body['statId'] = request.stat_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='QueryCandidates',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/candidates/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryCandidatesResponse(),
            await self.execute_async(params, req, runtime)
        )

    def query_candidates(
        self,
        request: dingtalkats__1__0_models.QueryCandidatesRequest,
    ) -> dingtalkats__1__0_models.QueryCandidatesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryCandidatesHeaders()
        return self.query_candidates_with_options(request, headers, runtime)

    async def query_candidates_async(
        self,
        request: dingtalkats__1__0_models.QueryCandidatesRequest,
    ) -> dingtalkats__1__0_models.QueryCandidatesResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryCandidatesHeaders()
        return await self.query_candidates_with_options_async(request, headers, runtime)

    def query_interviews_with_options(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
        headers: dingtalkats__1__0_models.QueryInterviewsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.next_token):
            query['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        body = {}
        if not UtilClient.is_unset(request.candidate_id):
            body['candidateId'] = request.candidate_id
        if not UtilClient.is_unset(request.start_time_begin_millis):
            body['startTimeBeginMillis'] = request.start_time_begin_millis
        if not UtilClient.is_unset(request.start_time_end_millis):
            body['startTimeEndMillis'] = request.start_time_end_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='QueryInterviews',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/interviews/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryInterviewsResponse(),
            self.execute(params, req, runtime)
        )

    async def query_interviews_with_options_async(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
        headers: dingtalkats__1__0_models.QueryInterviewsHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.next_token):
            query['nextToken'] = request.next_token
        if not UtilClient.is_unset(request.size):
            query['size'] = request.size
        body = {}
        if not UtilClient.is_unset(request.candidate_id):
            body['candidateId'] = request.candidate_id
        if not UtilClient.is_unset(request.start_time_begin_millis):
            body['startTimeBeginMillis'] = request.start_time_begin_millis
        if not UtilClient.is_unset(request.start_time_end_millis):
            body['startTimeEndMillis'] = request.start_time_end_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='QueryInterviews',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/interviews/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.QueryInterviewsResponse(),
            await self.execute_async(params, req, runtime)
        )

    def query_interviews(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryInterviewsHeaders()
        return self.query_interviews_with_options(request, headers, runtime)

    async def query_interviews_async(
        self,
        request: dingtalkats__1__0_models.QueryInterviewsRequest,
    ) -> dingtalkats__1__0_models.QueryInterviewsResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.QueryInterviewsHeaders()
        return await self.query_interviews_with_options_async(request, headers, runtime)

    def report_message_status_with_options(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
        headers: dingtalkats__1__0_models.ReportMessageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.message_id):
            body['messageId'] = request.message_id
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReportMessageStatus',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/messages/statuses/report',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ReportMessageStatusResponse(),
            self.execute(params, req, runtime)
        )

    async def report_message_status_with_options_async(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
        headers: dingtalkats__1__0_models.ReportMessageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.message_id):
            body['messageId'] = request.message_id
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReportMessageStatus',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/messages/statuses/report',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.ReportMessageStatusResponse(),
            await self.execute_async(params, req, runtime)
        )

    def report_message_status(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ReportMessageStatusHeaders()
        return self.report_message_status_with_options(request, headers, runtime)

    async def report_message_status_async(
        self,
        request: dingtalkats__1__0_models.ReportMessageStatusRequest,
    ) -> dingtalkats__1__0_models.ReportMessageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.ReportMessageStatusHeaders()
        return await self.report_message_status_with_options_async(request, headers, runtime)

    def sync_channel_message_with_options(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
        headers: dingtalkats__1__0_models.SyncChannelMessageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.create_time):
            body['createTime'] = request.create_time
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        if not UtilClient.is_unset(request.uuid):
            body['uuid'] = request.uuid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncChannelMessage',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/messages/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.SyncChannelMessageResponse(),
            self.execute(params, req, runtime)
        )

    async def sync_channel_message_with_options_async(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
        headers: dingtalkats__1__0_models.SyncChannelMessageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.channel):
            body['channel'] = request.channel
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.create_time):
            body['createTime'] = request.create_time
        if not UtilClient.is_unset(request.receiver_user_id):
            body['receiverUserId'] = request.receiver_user_id
        if not UtilClient.is_unset(request.sender_user_id):
            body['senderUserId'] = request.sender_user_id
        if not UtilClient.is_unset(request.uuid):
            body['uuid'] = request.uuid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncChannelMessage',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/channels/messages/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.SyncChannelMessageResponse(),
            await self.execute_async(params, req, runtime)
        )

    def sync_channel_message(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.SyncChannelMessageHeaders()
        return self.sync_channel_message_with_options(request, headers, runtime)

    async def sync_channel_message_async(
        self,
        request: dingtalkats__1__0_models.SyncChannelMessageRequest,
    ) -> dingtalkats__1__0_models.SyncChannelMessageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.SyncChannelMessageHeaders()
        return await self.sync_channel_message_with_options_async(request, headers, runtime)

    def update_application_reg_form_with_options(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
        headers: dingtalkats__1__0_models.UpdateApplicationRegFormHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.ding_pan_file):
            body['dingPanFile'] = request.ding_pan_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateApplicationRegForm',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/{flow_id}/applicationRegForms',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateApplicationRegFormResponse(),
            self.execute(params, req, runtime)
        )

    async def update_application_reg_form_with_options_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
        headers: dingtalkats__1__0_models.UpdateApplicationRegFormHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.content):
            body['content'] = request.content
        if not UtilClient.is_unset(request.ding_pan_file):
            body['dingPanFile'] = request.ding_pan_file
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateApplicationRegForm',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/flows/{flow_id}/applicationRegForms',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateApplicationRegFormResponse(),
            await self.execute_async(params, req, runtime)
        )

    def update_application_reg_form(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateApplicationRegFormHeaders()
        return self.update_application_reg_form_with_options(flow_id, request, headers, runtime)

    async def update_application_reg_form_async(
        self,
        flow_id: str,
        request: dingtalkats__1__0_models.UpdateApplicationRegFormRequest,
    ) -> dingtalkats__1__0_models.UpdateApplicationRegFormResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateApplicationRegFormHeaders()
        return await self.update_application_reg_form_with_options_async(flow_id, request, headers, runtime)

    def update_interview_sign_in_info_with_options(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
        headers: dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.sign_in_time_millis):
            body['signInTimeMillis'] = request.sign_in_time_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateInterviewSignInInfo',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/interviews/{interview_id}/signInInfos',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse(),
            self.execute(params, req, runtime)
        )

    async def update_interview_sign_in_info_with_options_async(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
        headers: dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        body = {}
        if not UtilClient.is_unset(request.sign_in_time_millis):
            body['signInTimeMillis'] = request.sign_in_time_millis
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateInterviewSignInInfo',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/interviews/{interview_id}/signInInfos',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse(),
            await self.execute_async(params, req, runtime)
        )

    def update_interview_sign_in_info(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders()
        return self.update_interview_sign_in_info_with_options(interview_id, request, headers, runtime)

    async def update_interview_sign_in_info_async(
        self,
        interview_id: str,
        request: dingtalkats__1__0_models.UpdateInterviewSignInInfoRequest,
    ) -> dingtalkats__1__0_models.UpdateInterviewSignInInfoResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateInterviewSignInInfoHeaders()
        return await self.update_interview_sign_in_info_with_options_async(interview_id, request, headers, runtime)

    def update_job_deliver_with_options(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
        headers: dingtalkats__1__0_models.UpdateJobDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.job_id):
            query['jobId'] = request.job_id
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.deliver_user_id):
            body['deliverUserId'] = request.deliver_user_id
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.op_time):
            body['opTime'] = request.op_time
        if not UtilClient.is_unset(request.op_user_id):
            body['opUserId'] = request.op_user_id
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateJobDeliver',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/jobs/deliveryStatus',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateJobDeliverResponse(),
            self.execute(params, req, runtime)
        )

    async def update_job_deliver_with_options_async(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
        headers: dingtalkats__1__0_models.UpdateJobDeliverHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_code):
            query['bizCode'] = request.biz_code
        if not UtilClient.is_unset(request.job_id):
            query['jobId'] = request.job_id
        body = {}
        if not UtilClient.is_unset(request.channel_outer_id):
            body['channelOuterId'] = request.channel_outer_id
        if not UtilClient.is_unset(request.deliver_user_id):
            body['deliverUserId'] = request.deliver_user_id
        if not UtilClient.is_unset(request.error_code):
            body['errorCode'] = request.error_code
        if not UtilClient.is_unset(request.error_msg):
            body['errorMsg'] = request.error_msg
        if not UtilClient.is_unset(request.op_time):
            body['opTime'] = request.op_time
        if not UtilClient.is_unset(request.op_user_id):
            body['opUserId'] = request.op_user_id
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UpdateJobDeliver',
            version='ats_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/ats/jobs/deliveryStatus',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkats__1__0_models.UpdateJobDeliverResponse(),
            await self.execute_async(params, req, runtime)
        )

    def update_job_deliver(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateJobDeliverHeaders()
        return self.update_job_deliver_with_options(request, headers, runtime)

    async def update_job_deliver_async(
        self,
        request: dingtalkats__1__0_models.UpdateJobDeliverRequest,
    ) -> dingtalkats__1__0_models.UpdateJobDeliverResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkats__1__0_models.UpdateJobDeliverHeaders()
        return await self.update_job_deliver_with_options_async(request, headers, runtime)
