"""
Tencent is pleased to support the open source community by making BK-LOG 蓝鲸日志平台 available.
Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
BK-LOG 蓝鲸日志平台 is licensed under the MIT License.
License for BK-LOG 蓝鲸日志平台:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF  OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
We undertake not to change the open source license (MIT license) applicable to the current version of
the project delivered to anyone in the future.
"""

from rest_framework import serializers
from rest_framework.response import Response

from apps.generic import APIViewSet
from apps.iam import ActionEnum, ResourceEnum
from apps.iam.handlers.drf import InstanceActionPermission
from apps.log_clustering.handlers.pattern import PatternHandler
from apps.log_clustering.serializers import (
    DeleteRemarkSerializer,
    PatternSearchSerlaizer,
    SetLabelSerializer,
    SetOwnerSerializer,
    SetRemarkSerializer,
    UpdateRemarkSerializer,
)
from apps.utils.drf import detail_route


class PatternViewSet(APIViewSet):
    lookup_field = "index_set_id"
    serializer_class = serializers.Serializer

    def get_permissions(self):
        return [InstanceActionPermission([ActionEnum.SEARCH_LOG], ResourceEnum.INDICES)]

    @detail_route(methods=["POST"])
    def search(self, request, index_set_id):
        """
        @api {post} /pattern/$index_set_id/search/ 日志聚类-聚类检索
        @apiName pattern_search
        @apiGroup log_clustering
        @apiParam {String} pattern_level 聚类敏感度 01 03 05 06 07 08
        @apiParam {String} start_time 开始时间
        @apiParam {String} end_time 结束时间
        @apiParam {String} time_range 时间标识符符["15m", "30m", "1h", "4h", "12h", "1d", "customized"]
        @apiParam {String} keyword 搜索关键字
        @apiParam {Json} ip IP列表
        @apiParam {Json} addition 搜索条件
        @apiParam {Int} year_on_year_hour 同比周期 单位小时 n小时前
        @apiParam {Int} size 条数
        @apiParam {Array} group_by 分组字段
        @apiParamExample {Json} 请求参数
        {
            "year_on_year_hour": 1,
            "pattern_level": "01",
            "start_time": "2019-06-11 00:00:00",
            "end_time": "2019-06-12 11:11:11",
            "time_range": "customized"
            "keyword": "error",
            "group_by": ["serverIp", "cloudId", ....],
            "host_scopes": {
            "modules": [
                {
                    "bk_obj_id": "module",
                    "bk_inst_id": 4
                },
                {
                    "bk_obj_id": "set",
                    "bk_inst_id": 4
                }
            ],
            "ips": "127.0.0.1, 127.0.0.2"
            },
            "addition": [
                {
                "key": "ip",
                "method": "is",
                "value": "127.0.0.1",
                "condition": "and", (默认不传是and，只支持and or)
                "type": "field"(默认field
                    目前支持field，其他无效)
                }
            ],
        }
        @apiSuccessExample {json} 成功返回:
        {
            "message": "",
            "code": 0,
            "data": [
                {
                    "pattern": "xx [ip] [xxxxx] xxxxx]",
                    "signature": "xxxxxxxxxxxx",
                    "count": 123,
                    "year_on_year": -10,
                    "percentage": 12,
                    "is_new_class": true,
                    "year_on_year_count": 12,
                    "year_on_year_percentage": 10,
                    "labels": ["xxxx", "xxxx"],
                    "remark": "xxxx",
                    "group": ["xxx"],
                    "monitor":
                    {
                    "is_active": true,
                    "strategy_id": 1,
                    }
                }
            ],
            "result": true
        }
        """
        query_data = self.params_valid(PatternSearchSerlaizer)
        return Response(PatternHandler(index_set_id, query_data).pattern_search())

    @detail_route(methods=["POST"], url_path="label")
    def set_label(self, request, index_set_id):
        """
        @api {post} /pattern/$index_set_id/label/ 日志聚类-设置标签
        @apiName set_label
        @apiGroup log_clustering
        @apiParam {String} signature 数据指纹
        @apiParam {String} label 标签内容
        @apiSuccessExample {json} 成功返回: null
        """
        params = self.params_valid(SetLabelSerializer)
        return Response(
            PatternHandler(index_set_id, {}).set_signature_config(
                signature=params["signature"], configs={"label": params["label"]}
            )
        )

    @detail_route(methods=["POST"], url_path="remark")
    def set_remark(self, request, index_set_id):
        """
        @api {post} /pattern/$index_set_id/remark/ 日志聚类-设置备注
        @apiName set_remark
        @apiGroup log_clustering
        @apiParam {String} signature 数据指纹
        @apiParam {String} remark 备注内容
        @apiParamExample {json} 请求参数
        {
          "signature": "456",
          "remark": "备注信息"
        }
        @apiSuccessExample {json} 成功返回:
        {
            "result": true,
            "data": {
                "id": 1,
                "created_at": "2023-11-03T08:02:44.675115Z",
                "created_by": "xxx",
                "updated_at": "2023-11-09T02:44:58.997461Z",
                "updated_by": "xxx",
                "is_deleted": false,
                "deleted_at": null,
                "deleted_by": null,
                "model_id": "xxx_xxx_xxx",
                "signature": "456",
                "pattern": "",
                "label": "合并label",
                "remark": [
                    {
                        "remark": "合并label",
                        "username": "",
                        "create_time": 0
                    },
                    {
                        "username": "xxx",
                        "create_time": 1699497898000,
                        "remark": "备注信息"
                    }
                ],
                "owners": []
            },
            "code": 0,
            "message": ""
        }
        """
        params = self.params_valid(SetRemarkSerializer)
        return Response(
            PatternHandler(index_set_id, {}).set_clustering_remark(
                signature=params["signature"], configs={"remark": params["remark"]}, method="create"
            )
        )

    @detail_route(methods=["PUT"], url_path="update_remark")
    def update_remark(self, request, index_set_id):
        """
        @api {post} /pattern/$index_set_id/remark/edit/ 日志聚类-编辑备注
        @apiName set_remark
        @apiGroup log_clustering
        @apiParam {String} signature 数据指纹
        @apiParam {String} remark 备注内容
        @apiParamExample {json} 请求参数
        {
          "signature": "456",
          "old_remark": "备注信息",
          "new_remark": "新备注信息",
          "create_time": 1699497898000
        }
        @apiSuccessExample {json} 成功返回:
        {
            "result": true,
            "data": {
                "id": 1,
                "created_at": "2023-11-03T08:02:44.675115Z",
                "created_by": "xxx",
                "updated_at": "2023-11-09T02:44:58.997461Z",
                "updated_by": "xxx",
                "is_deleted": false,
                "deleted_at": null,
                "deleted_by": null,
                "model_id": "xxx_xxx_xxx",
                "signature": "456",
                "pattern": "",
                "label": "合并label",
                "remark": [
                    {
                        "remark": "合并label",
                        "username": "xxx",
                        "create_time": 1699497898000
                    },
                    {
                        "username": "xxx",
                        "create_time": 1699497898000,
                        "remark": "备注信息"
                    }
                ],
                "owners": []
            },
            "code": 0,
            "message": ""
        }
        """
        params = self.params_valid(UpdateRemarkSerializer)
        return Response(
            PatternHandler(index_set_id, {}).set_clustering_remark(
                signature=params["signature"],
                configs={
                    "old_remark": params["old_remark"],
                    "new_remark": params["new_remark"],
                    "create_time": params["create_time"],
                },
                method="update",
            )
        )

    @detail_route(methods=["DELETE"], url_path="delete_remark")
    def delete_remark(self, request, index_set_id):
        """
        @api {delete} /pattern/$index_set_id/remark/ 日志聚类-删除备注
        @apiName delete_remark
        @apiGroup log_clustering
        @apiParam {String} signature 数据指纹
        @apiParam {String} remark 备注内容
        @apiParamExample {json} 请求参数
        {
          "signature": "456",
          "remark": "备注信息"
          "create_time": 1699497898000
        }
        @apiSuccessExample {json} 成功返回:
        {
            "result": true,
            "data": {
                "id": 1,
                "created_at": "2023-11-03T08:02:44.675115Z",
                "created_by": "xxx",
                "updated_at": "2023-11-09T02:44:58.997461Z",
                "updated_by": "xxx",
                "is_deleted": false,
                "deleted_at": null,
                "deleted_by": null,
                "model_id": "xxx_xxx_xxx",
                "signature": "456",
                "pattern": "",
                "label": "合并label",
                "remark": [
                    {
                        "remark": "合并label",
                        "username": "",
                        "create_time": 0
                    },
                    {
                        "username": "xxx",
                        "create_time": 1699497898000,
                        "remark": "备注信息"
                    }
                ],
                "owners": []
            },
            "code": 0,
            "message": ""
        }
        """
        params = self.params_valid(DeleteRemarkSerializer)
        return Response(
            PatternHandler(index_set_id, {}).set_clustering_remark(
                signature=params["signature"],
                configs={"remark": params["remark"], "create_time": params["create_time"]},
                method="delete",
            )
        )

    @detail_route(methods=["POST"], url_path="owner")
    def set_owner(self, request, index_set_id):
        """
        @api {post} /pattern/$index_set_id/owner/ 日志聚类-设置负责人
        @apiName set_owner
        @apiGroup log_clustering
        @apiParam {String} signature 数据指纹
        @apiParam {String} owner 负责人
        @apiParamExample {json} 请求参数
        {
          "signature": "123",
          "owners": ["xxx", "xxx"]
        }
        @apiSuccessExample {json} 成功返回:
        {
            "result": true,
            "data": {
                "id": 1,
                "created_at": "2023-11-03T08:02:44.675115Z",
                "created_by": "xxx",
                "updated_at": "2023-11-09T02:44:58.997461Z",
                "updated_by": "xxx",
                "is_deleted": false,
                "deleted_at": null,
                "deleted_by": null,
                "model_id": "xxx_xxx_xxx",
                "signature": "123",
                "pattern": "",
                "label": "",
                "remark": [],
                "owners": ["xxx", "xxx"]
            },
            "code": 0,
            "message": ""
        }
        """
        params = self.params_valid(SetOwnerSerializer)
        return Response(
            PatternHandler(index_set_id, {}).set_signature_config(
                signature=params["signature"], configs={"owners": params["owners"]}
            )
        )
