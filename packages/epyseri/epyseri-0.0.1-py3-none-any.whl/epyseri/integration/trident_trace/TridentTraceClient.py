from typing import Optional
from .core import CoreAPI
import numpy as np
from .helper import FeaturesImage
from .utils import convert_data
from .schemas import MetadataVisionSchema
import json

class TridentTraceClient:
    def __init__(
            self, 
            base_url: str, 
            auth_token: str = None,
            app_name: str = None,
        ) -> None:  
        """
        Initializes the TridentTraceClient object.

        Parameters:
            - base_url (str): Base URL of the Trident Trace service.
            - auth_token (str): Authentication token, default is None.
            - app_name (str): Application name, default is None.
            - user (str): User name, default is None.

        Returns:
            None
        """
        self.base_url: str = base_url
        self.auth_token: str = auth_token
        self.app_name = app_name
        self.core = CoreAPI(base_url=self.base_url, auth_token=self.auth_token)
        self.service_domain_id = None
        self.service_domain_slug = None

        self.initialize()

    def __auto_setup(self, app_name):
        """
        Automatically sets up the service domain based on the app_name.

        Parameters:
            - app_name (str): Application name.

        Returns:
            Tuple[int, str]: A tuple containing domain_id and domain_slug.
        """
        domain_id, domain_slug = self.__get_domain(app_name)
        if domain_id is None:
            domain_slug_res = self.__post_domain(app_name)
            domain_id, domain_slug = self.__get_domain(domain_slug_res)
        return domain_id, domain_slug

    def initialize(self):
        """
        Initializes service_domain_id and service_domain_slug if app_name is specified.
        """
        if self.app_name:
            self.service_domain_id, self.service_domain_slug = self.__auto_setup(self.app_name)
        

    def get_health(self) -> dict | str:
        """
        Retrieves health information from the specified URL using httpx.

        Returns:
            Any: Response data.

        Basic Usage:
            >>> result = get_health()
            >>> print(result)
        """
        health_data = self.core.get_health()
        return health_data
        
        
    def __get_domain(self, app_name: str) -> dict | str:
        """
        Layanan DOMAIN - Mendapatkan detail domain berdasarkan app_name.

        Parameters:
            - app_name (str): Nama aplikasi.

        Returns:
            Any: Data respons atau pesan kesalahan.
        """
        domain_get_data = self.core.get_domain(app_name)
        return domain_get_data
        
    def __post_domain(self, app_name: str) -> dict | str:
        """
        DOMAIN SERVICE - Creates a new domain with the given app_name.

        Parameters:
            - app_name (str): Application name.

        Returns:
            Any: Response data.
        """
        domain_post_data = self.core.post_domain(app_name)
        return domain_post_data
        
    def delete_domain(self, domain_id: int) -> dict | str:
        """
        Deletes a domain with the specified domain_id.

        Parameters:
            - domain_id: Identifier of the domain to be deleted.

        Returns:
            Any: Response data.
        """
        domain_delete_data = self.core.delete_domain(domain_id)
        return domain_delete_data
        
    def get_list_inference(
            self,
            business_domain: str,
            limit: int = None,
            offset: int = None,
            service_domain_id: Optional[int] = None,
            service_domain_slug: Optional[str] = None,
            ai_domain: str = None,
            ai_subdomain: str = None,
            user: str = None,
            group_id: str = None,
            order_by: str = None
        ):
        """
        INFERENCE SERVICES - Get a list of inferences based on specified parameters.

        Parameters:
            - business_domain (str): Business domain.
            - limit (int): Maximum number of results to return.
            - offset (int): Result offset.

        Returns:
            Any: Response data.
        """
        inference_get_list_data = self.core.get_list_inference(
            business_domain=business_domain,
            limit=limit,
            offset=offset,
            service_domain_id=service_domain_id,
            service_domain_slug=service_domain_slug,
            ai_domain=ai_domain,
            ai_subdomain=ai_subdomain,
            user=user,
            group_id=group_id,
            order_by=order_by
        )
        # inference_get_list_data_result = convert_data(inference_get_list_data)
        return inference_get_list_data
        
    def get_detail_inference(self, inference_uuid) -> dict | str:
        """
        INFERENCE SERVICES - Get detailed information about a specific inference.

        Parameters:
            - inference_uuid: Identifier of the inference.

        Returns:
            Any: Response data.
        """
        inference_get_detail_data_result = self.core.get_detail_inference(inference_uuid)
        if inference_get_detail_data_result:
            for d_feed in inference_get_detail_data_result['data']['feedbacks']:
                comments = d_feed['user_comment']
                if "{" in comments[0] and  "}" in comments[-1]:
                    d_feed['user_comment'] = json.loads(comments)
        return inference_get_detail_data_result
    
    def post_inference(
            self,
            data_input: str | dict,
            data_output: str | dict,
            inference_time: int,
            ai_domain: str,
            ai_subdomain: str,
            model_version: str,
            business_domain: str,
            user: str, 
            image: np.ndarray | str | None = None, 
            group_id: str | None = None,
            service_domain_id: int | None = None,
            conf_thershold: float | None = None
        ) -> dict | str:
        """
        INFERENCE SERVICES - Create a new inference with the specified parameters.

        Parameters:
            - data_input: Input data for the inference.
            - data_output: Output data for the inference.
            - inference_time: Time of the inference.
            - ...

        Returns:
            Any: Response data.
        """
        meta_data_vision = None
        if isinstance(image, np.ndarray):
            meta_data_vision = FeaturesImage.compute_features(image)
            meta_data_vision['confidence_threshold'] = conf_thershold
            meta_data_vision = MetadataVisionSchema(**meta_data_vision)

        if isinstance(data_input, dict):
            data_input = json.dumps(data_input)

        if isinstance(data_output, dict):
            data_output = json.dumps(data_output)

        body = {
            "data_input": data_input,
            "data_output": data_output,
            "inference_time": inference_time,
            "business_domain": business_domain,
            "service_domain_id": service_domain_id or self.service_domain_id,
            "ai_domain": ai_domain,
            "ai_subdomain": ai_subdomain,
            "model_version": model_version,
            "user": user 
        }
        if meta_data_vision:
            body["meta_data_vision"] = meta_data_vision.model_dump()
        if group_id:
            body["group_id"] = group_id
        inference_create_data = self.core.post_inference(body)
        return inference_create_data

    def delete_inference(self, inference_uuid: str) -> dict | str:
        """
        INFERENCE SERVICES - Delete an inference with the specified inference_uuid.

        Parameters:
            - inference_uuid: Identifier of the inference to be deleted.

        Returns:
            Any: Response data.
        """
        inference_delete_data = self.core.delete_inference(inference_uuid)
        return inference_delete_data
        
    def get_group_inference(
            self,
            business_domain: str,
            user: str = None,
            limit: int = None,
            offset: int = None,
            service_domain_id: Optional[int] = None,
            service_domain_slug: Optional[str] = None,
            ai_domain: str = None,
            ai_subdomain: str = None,
            group_id: str = None,
            start_date: str = None,
            end_date: str = None
        ):
            """
            INFERENCE SERVICES - Get a list of group inferences based on specified parameters.

            Parameters:
                - business_domain (str): Business domain.
                - limit (int): Maximum number of results to return.
                - offset (int): Result offset.
                - ...

            Returns:
                Any: Response data.
            """
            inference_get_group_data = self.core.get_group_inference(
                business_domain = business_domain,
                limit = limit,
                offset = offset,
                service_domain_id = service_domain_id,
                service_domain_slug = service_domain_slug,
                ai_domain = ai_domain,
                ai_subdomain = ai_subdomain,
                user = user,
                group_id = group_id,
                start_date = start_date,
                end_date = end_date
            )

            inference_get_group_data_result = convert_data(inference_get_group_data)
            return inference_get_group_data_result

            
    def get_detail_group_inference(self, group_id: str):
        """
        INFERENCE SERVICES - Get detailed information about a specific group inference.

        Parameters:
            - group_id: Identifier of the group inference.

        Returns:
            Any: Response data.
        """
        inference_get_detail_group_data = self.core.get_detail_group_inference(group_id)
        return inference_get_detail_group_data
        

    def post_feedback(
            self, 
            inference_uuid, 
            user_reaction, 
            user_comment: str | dict, 
            user=None
        ):
        """
        FEEDBACK SERVICE - Create feedback for a specific inference.

        Parameters:
            - inference_uuid: Identifier of the associated inference.
            - user_reaction: User's reaction to the inference.
            - user_comment: User's comment on the inference.

        Returns:
            Any: Response data.
        """
        feedback_create_data = self.core.post_feedback(
            inference_uuid = inference_uuid, 
            user_reaction = user_reaction, 
            user_comment = user_comment, 
            user = user 
        )
        return feedback_create_data
        
    def update_feedback(
            self, 
            uuid, 
            inference_uuid, 
            user_reaction: bool, 
            user_comment: str | dict, 
            user=None
        ):
        """
        FEEDBACK SERVICE - Update feedback with the specified parameters.

        Parameters:
            - uuid: Identifier of the feedback.
            - inference_uuid: Identifier of the associated inference.
            - user_reaction: User's updated reaction to the inference.
            - user_comment: User's updated comment on the inference.

        Returns:
            Any: Response data.
        """
        feedback_update_data = self.core.update_feedback(
            uuid = uuid,
            inference_uuid = inference_uuid, 
            user_reaction = user_reaction, 
            user_comment = user_comment, 
            user = user 
        )
        return feedback_update_data
    
class AsyncTridentTraceClien:
    pass
