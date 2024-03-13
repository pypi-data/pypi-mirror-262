# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class BatchModifyDomainInfoRequest(AbstractModel):
    """BatchModifyDomainInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 批量修改的域名。
        :type Domains: list of str
        :param _TemplateId: 模板ID。
        :type TemplateId: str
        :param _LockTransfer: true： 开启60天内禁止转移注册商锁定
false：关闭60天内禁止转移注册商锁定
默认 true
        :type LockTransfer: bool
        """
        self._Domains = None
        self._TemplateId = None
        self._LockTransfer = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def LockTransfer(self):
        return self._LockTransfer

    @LockTransfer.setter
    def LockTransfer(self, LockTransfer):
        self._LockTransfer = LockTransfer


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._TemplateId = params.get("TemplateId")
        self._LockTransfer = params.get("LockTransfer")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BatchModifyDomainInfoResponse(AbstractModel):
    """BatchModifyDomainInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class BatchStatus(AbstractModel):
    """批量任务状态

    """

    def __init__(self):
        r"""
        :param _LogId: 批量任务id
        :type LogId: int
        :param _Status: 批量任务状态  doing：进行中  success：成功  failed：失败  partial_success：部分成功
        :type Status: str
        :param _BatchAction: 批量任务类型
        :type BatchAction: str
        """
        self._LogId = None
        self._Status = None
        self._BatchAction = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def BatchAction(self):
        return self._BatchAction

    @BatchAction.setter
    def BatchAction(self, BatchAction):
        self._BatchAction = BatchAction


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._Status = params.get("Status")
        self._BatchAction = params.get("BatchAction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CertificateInfo(AbstractModel):
    """认证资料信息

    """

    def __init__(self):
        r"""
        :param _CertificateCode: 证件号码。
        :type CertificateCode: str
        :param _CertificateType: 证件类型。
SFZ: 身份证。
HZ: 护照。
TXZ: 中国港澳居民来往内地通行证。
TWSFZ: 中国台湾居民来往大陆通行证。
GWSFZ: 外国人永久居留身份证。
ORG: 组织机构代码证
YYZZ: 工商营业执照。
TYDMZ: 统一社会信用代码证书。
BDDH: 部队代号
JDXKZ: 军队单位对外有偿服务许可证。
SYZS: 事业单位法定代表人证书。
GWCZDJZ: 外国企业常驻代表机构登记证。
STDJZ: 社会团体法定代表人登记证书。
ZJDJZ: 宗教活动场所登记证。
MBDJZ: 民办非企业单位登记证书。
JJDJZ: 基金会法定代表人登记证书。
LSXKZ: 律师事务所执业许可证。
GWZHDJZ: 外国在华文化中心登记证。
GWLYDJZ: 外国政府旅游部门常驻代表机构批准登记证。
SFXKZ: 司法鉴定许可证
GWJGZJ: 外国机构证件。
SHFWJGZ: 社会服务机构登记证书。
MBXXXKZ: 民办学校办学许可证。
YLJGXKZ: 医疗机构执业许可证。
GAJZZ: 中国港澳居住证。
TWJZZ: 中国台湾居住证。
QTTYDM: 其他-统一社会信用代码证书。
GZJGZY: 公证机构执业证。
        :type CertificateType: str
        :param _ImgUrl: 证件照片地址。
        :type ImgUrl: str
        :param _OriginImgUrl: 原始照片地址
注意：此字段可能返回 null，表示取不到有效值。
        :type OriginImgUrl: str
        :param _RegistrantCertificateCode: 联系人证件号码。
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistrantCertificateCode: str
        :param _RegistrantCertificateType: 联系人证件类型。
SFZ: 身份证。
HZ: 护照。
TXZ: 中国港澳居民来往内地通行证。
TWSFZ: 中国台湾居民来往大陆通行证。
GWSFZ: 外国人永久居留身份证。
ORG: 组织机构代码证
YYZZ: 工商营业执照。
TYDMZ: 统一社会信用代码证书。
BDDH: 部队代号
JDXKZ: 军队单位对外有偿服务许可证。
SYZS: 事业单位法定代表人证书。
GWCZDJZ: 外国企业常驻代表机构登记证。
STDJZ: 社会团体法定代表人登记证书。
ZJDJZ: 宗教活动场所登记证。
MBDJZ: 民办非企业单位登记证书。
JJDJZ: 基金会法定代表人登记证书。
LSXKZ: 律师事务所执业许可证。
GWZHDJZ: 外国在华文化中心登记证。
GWLYDJZ: 外国政府旅游部门常驻代表机构批准登记证。
SFXKZ: 司法鉴定许可证
GWJGZJ: 外国机构证件。
SHFWJGZ: 社会服务机构登记证书。
MBXXXKZ: 民办学校办学许可证。
YLJGXKZ: 医疗机构执业许可证。
GAJZZ: 中国港澳居住证。
TWJZZ: 中国台湾居住证。
QTTYDM: 其他-统一社会信用代码证书。
GZJGZY: 公证机构执业证。
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistrantCertificateType: str
        :param _RegistrantImgUrl: 联系人证件照片地址。
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistrantImgUrl: str
        """
        self._CertificateCode = None
        self._CertificateType = None
        self._ImgUrl = None
        self._OriginImgUrl = None
        self._RegistrantCertificateCode = None
        self._RegistrantCertificateType = None
        self._RegistrantImgUrl = None

    @property
    def CertificateCode(self):
        return self._CertificateCode

    @CertificateCode.setter
    def CertificateCode(self, CertificateCode):
        self._CertificateCode = CertificateCode

    @property
    def CertificateType(self):
        return self._CertificateType

    @CertificateType.setter
    def CertificateType(self, CertificateType):
        self._CertificateType = CertificateType

    @property
    def ImgUrl(self):
        return self._ImgUrl

    @ImgUrl.setter
    def ImgUrl(self, ImgUrl):
        self._ImgUrl = ImgUrl

    @property
    def OriginImgUrl(self):
        return self._OriginImgUrl

    @OriginImgUrl.setter
    def OriginImgUrl(self, OriginImgUrl):
        self._OriginImgUrl = OriginImgUrl

    @property
    def RegistrantCertificateCode(self):
        return self._RegistrantCertificateCode

    @RegistrantCertificateCode.setter
    def RegistrantCertificateCode(self, RegistrantCertificateCode):
        self._RegistrantCertificateCode = RegistrantCertificateCode

    @property
    def RegistrantCertificateType(self):
        return self._RegistrantCertificateType

    @RegistrantCertificateType.setter
    def RegistrantCertificateType(self, RegistrantCertificateType):
        self._RegistrantCertificateType = RegistrantCertificateType

    @property
    def RegistrantImgUrl(self):
        return self._RegistrantImgUrl

    @RegistrantImgUrl.setter
    def RegistrantImgUrl(self, RegistrantImgUrl):
        self._RegistrantImgUrl = RegistrantImgUrl


    def _deserialize(self, params):
        self._CertificateCode = params.get("CertificateCode")
        self._CertificateType = params.get("CertificateType")
        self._ImgUrl = params.get("ImgUrl")
        self._OriginImgUrl = params.get("OriginImgUrl")
        self._RegistrantCertificateCode = params.get("RegistrantCertificateCode")
        self._RegistrantCertificateType = params.get("RegistrantCertificateType")
        self._RegistrantImgUrl = params.get("RegistrantImgUrl")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckBatchStatusRequest(AbstractModel):
    """CheckBatchStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param _LogIds: 操作日志 ID数组，最多 200 个
        :type LogIds: list of int non-negative
        """
        self._LogIds = None

    @property
    def LogIds(self):
        return self._LogIds

    @LogIds.setter
    def LogIds(self, LogIds):
        self._LogIds = LogIds


    def _deserialize(self, params):
        self._LogIds = params.get("LogIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckBatchStatusResponse(AbstractModel):
    """CheckBatchStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param _StatusSet: 批量任务状态集
        :type StatusSet: list of BatchStatus
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._StatusSet = None
        self._RequestId = None

    @property
    def StatusSet(self):
        return self._StatusSet

    @StatusSet.setter
    def StatusSet(self, StatusSet):
        self._StatusSet = StatusSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("StatusSet") is not None:
            self._StatusSet = []
            for item in params.get("StatusSet"):
                obj = BatchStatus()
                obj._deserialize(item)
                self._StatusSet.append(obj)
        self._RequestId = params.get("RequestId")


class CheckDomainRequest(AbstractModel):
    """CheckDomain请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainName: 所查询域名名称
        :type DomainName: str
        :param _Period: 年限。该参数为空时无法查询溢价词域名
        :type Period: str
        """
        self._DomainName = None
        self._Period = None

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period


    def _deserialize(self, params):
        self._DomainName = params.get("DomainName")
        self._Period = params.get("Period")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDomainResponse(AbstractModel):
    """CheckDomain返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainName: 所查询域名名称
        :type DomainName: str
        :param _Available: 是否能够注册
        :type Available: bool
        :param _Reason: 不能注册原因
        :type Reason: str
        :param _Premium: 是否是溢价词
        :type Premium: bool
        :param _Price: 域名价格
        :type Price: int
        :param _BlackWord: 是否是敏感词
        :type BlackWord: bool
        :param _Describe: 溢价词描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param _FeeRenew: 溢价词的续费价格
注意：此字段可能返回 null，表示取不到有效值。
        :type FeeRenew: int
        :param _RealPrice: 域名真实价格, 溢价词时价格跟年限有关，非溢价词时价格为1年的价格
注意：此字段可能返回 null，表示取不到有效值。
        :type RealPrice: int
        :param _FeeTransfer: 溢价词的转入价格
注意：此字段可能返回 null，表示取不到有效值。
        :type FeeTransfer: int
        :param _FeeRestore: 溢价词的赎回价格
        :type FeeRestore: int
        :param _Period: 检测年限
        :type Period: int
        :param _RecordSupport: 是否支持北京备案  true 支持  false 不支持
        :type RecordSupport: bool
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DomainName = None
        self._Available = None
        self._Reason = None
        self._Premium = None
        self._Price = None
        self._BlackWord = None
        self._Describe = None
        self._FeeRenew = None
        self._RealPrice = None
        self._FeeTransfer = None
        self._FeeRestore = None
        self._Period = None
        self._RecordSupport = None
        self._RequestId = None

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName

    @property
    def Available(self):
        return self._Available

    @Available.setter
    def Available(self, Available):
        self._Available = Available

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def Premium(self):
        return self._Premium

    @Premium.setter
    def Premium(self, Premium):
        self._Premium = Premium

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, Price):
        self._Price = Price

    @property
    def BlackWord(self):
        return self._BlackWord

    @BlackWord.setter
    def BlackWord(self, BlackWord):
        self._BlackWord = BlackWord

    @property
    def Describe(self):
        return self._Describe

    @Describe.setter
    def Describe(self, Describe):
        self._Describe = Describe

    @property
    def FeeRenew(self):
        return self._FeeRenew

    @FeeRenew.setter
    def FeeRenew(self, FeeRenew):
        self._FeeRenew = FeeRenew

    @property
    def RealPrice(self):
        return self._RealPrice

    @RealPrice.setter
    def RealPrice(self, RealPrice):
        self._RealPrice = RealPrice

    @property
    def FeeTransfer(self):
        return self._FeeTransfer

    @FeeTransfer.setter
    def FeeTransfer(self, FeeTransfer):
        self._FeeTransfer = FeeTransfer

    @property
    def FeeRestore(self):
        return self._FeeRestore

    @FeeRestore.setter
    def FeeRestore(self, FeeRestore):
        self._FeeRestore = FeeRestore

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def RecordSupport(self):
        return self._RecordSupport

    @RecordSupport.setter
    def RecordSupport(self, RecordSupport):
        self._RecordSupport = RecordSupport

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._DomainName = params.get("DomainName")
        self._Available = params.get("Available")
        self._Reason = params.get("Reason")
        self._Premium = params.get("Premium")
        self._Price = params.get("Price")
        self._BlackWord = params.get("BlackWord")
        self._Describe = params.get("Describe")
        self._FeeRenew = params.get("FeeRenew")
        self._RealPrice = params.get("RealPrice")
        self._FeeTransfer = params.get("FeeTransfer")
        self._FeeRestore = params.get("FeeRestore")
        self._Period = params.get("Period")
        self._RecordSupport = params.get("RecordSupport")
        self._RequestId = params.get("RequestId")


class ContactInfo(AbstractModel):
    """域名联系人信息

    """

    def __init__(self):
        r"""
        :param _OrganizationNameCN: 注册人（中文）
        :type OrganizationNameCN: str
        :param _OrganizationName: 注册人（英文）
        :type OrganizationName: str
        :param _RegistrantNameCN: 联系人（中文）
        :type RegistrantNameCN: str
        :param _RegistrantName: 联系人（英文）
        :type RegistrantName: str
        :param _ProvinceCN: 省份（中文）
        :type ProvinceCN: str
        :param _CityCN: 城市（中文）
        :type CityCN: str
        :param _StreetCN: 街道（中文）
        :type StreetCN: str
        :param _Street: 街道（英文）
        :type Street: str
        :param _CountryCN: 国家（中文）
        :type CountryCN: str
        :param _Telephone: 联系人手机号
        :type Telephone: str
        :param _Email: 联系人邮箱
        :type Email: str
        :param _ZipCode: 邮编
        :type ZipCode: str
        :param _RegistrantType: 用户类型 E:组织， I:个人
        :type RegistrantType: str
        :param _Province: 省份（英文）。作为入参时可以不填
        :type Province: str
        :param _City: 城市（英文）。作为入参时可以不填
        :type City: str
        :param _Country: 国家（英文）。作为入参时可以不填
        :type Country: str
        """
        self._OrganizationNameCN = None
        self._OrganizationName = None
        self._RegistrantNameCN = None
        self._RegistrantName = None
        self._ProvinceCN = None
        self._CityCN = None
        self._StreetCN = None
        self._Street = None
        self._CountryCN = None
        self._Telephone = None
        self._Email = None
        self._ZipCode = None
        self._RegistrantType = None
        self._Province = None
        self._City = None
        self._Country = None

    @property
    def OrganizationNameCN(self):
        return self._OrganizationNameCN

    @OrganizationNameCN.setter
    def OrganizationNameCN(self, OrganizationNameCN):
        self._OrganizationNameCN = OrganizationNameCN

    @property
    def OrganizationName(self):
        return self._OrganizationName

    @OrganizationName.setter
    def OrganizationName(self, OrganizationName):
        self._OrganizationName = OrganizationName

    @property
    def RegistrantNameCN(self):
        return self._RegistrantNameCN

    @RegistrantNameCN.setter
    def RegistrantNameCN(self, RegistrantNameCN):
        self._RegistrantNameCN = RegistrantNameCN

    @property
    def RegistrantName(self):
        return self._RegistrantName

    @RegistrantName.setter
    def RegistrantName(self, RegistrantName):
        self._RegistrantName = RegistrantName

    @property
    def ProvinceCN(self):
        return self._ProvinceCN

    @ProvinceCN.setter
    def ProvinceCN(self, ProvinceCN):
        self._ProvinceCN = ProvinceCN

    @property
    def CityCN(self):
        return self._CityCN

    @CityCN.setter
    def CityCN(self, CityCN):
        self._CityCN = CityCN

    @property
    def StreetCN(self):
        return self._StreetCN

    @StreetCN.setter
    def StreetCN(self, StreetCN):
        self._StreetCN = StreetCN

    @property
    def Street(self):
        return self._Street

    @Street.setter
    def Street(self, Street):
        self._Street = Street

    @property
    def CountryCN(self):
        return self._CountryCN

    @CountryCN.setter
    def CountryCN(self, CountryCN):
        self._CountryCN = CountryCN

    @property
    def Telephone(self):
        return self._Telephone

    @Telephone.setter
    def Telephone(self, Telephone):
        self._Telephone = Telephone

    @property
    def Email(self):
        return self._Email

    @Email.setter
    def Email(self, Email):
        self._Email = Email

    @property
    def ZipCode(self):
        return self._ZipCode

    @ZipCode.setter
    def ZipCode(self, ZipCode):
        self._ZipCode = ZipCode

    @property
    def RegistrantType(self):
        return self._RegistrantType

    @RegistrantType.setter
    def RegistrantType(self, RegistrantType):
        self._RegistrantType = RegistrantType

    @property
    def Province(self):
        return self._Province

    @Province.setter
    def Province(self, Province):
        self._Province = Province

    @property
    def City(self):
        return self._City

    @City.setter
    def City(self, City):
        self._City = City

    @property
    def Country(self):
        return self._Country

    @Country.setter
    def Country(self, Country):
        self._Country = Country


    def _deserialize(self, params):
        self._OrganizationNameCN = params.get("OrganizationNameCN")
        self._OrganizationName = params.get("OrganizationName")
        self._RegistrantNameCN = params.get("RegistrantNameCN")
        self._RegistrantName = params.get("RegistrantName")
        self._ProvinceCN = params.get("ProvinceCN")
        self._CityCN = params.get("CityCN")
        self._StreetCN = params.get("StreetCN")
        self._Street = params.get("Street")
        self._CountryCN = params.get("CountryCN")
        self._Telephone = params.get("Telephone")
        self._Email = params.get("Email")
        self._ZipCode = params.get("ZipCode")
        self._RegistrantType = params.get("RegistrantType")
        self._Province = params.get("Province")
        self._City = params.get("City")
        self._Country = params.get("Country")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCustomDnsHostRequest(AbstractModel):
    """CreateCustomDnsHost请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名实例ID
        :type DomainId: str
        :param _DnsName: Dns名称
        :type DnsName: str
        :param _IpSet: IP地址列表
        :type IpSet: list of str
        """
        self._DomainId = None
        self._DnsName = None
        self._IpSet = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DnsName(self):
        return self._DnsName

    @DnsName.setter
    def DnsName(self, DnsName):
        self._DnsName = DnsName

    @property
    def IpSet(self):
        return self._IpSet

    @IpSet.setter
    def IpSet(self, IpSet):
        self._IpSet = IpSet


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DnsName = params.get("DnsName")
        self._IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCustomDnsHostResponse(AbstractModel):
    """CreateCustomDnsHost返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 异步任务ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class CreateDomainBatchRequest(AbstractModel):
    """CreateDomainBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID。详情请查看：[获取模板列表](https://cloud.tencent.com/document/product/242/48940)
        :type TemplateId: str
        :param _Period: 购买域名的年限，可选值：[1-10]
        :type Period: int
        :param _Domains: 批量购买的域名,最多为4000个
        :type Domains: list of str
        :param _PayMode: 付费模式 0手动在线付费，1使用余额付费，2使用特惠包
        :type PayMode: int
        :param _AutoRenewFlag: 自动续费开关。有两个可选值：
0 表示关闭，不自动续费（默认值）
1 表示开启，将自动续费
        :type AutoRenewFlag: int
        :param _PackageResourceId: 使用的特惠包ID，PayMode为2时必填
        :type PackageResourceId: str
        :param _UpdateProhibition: 是否开启更新锁：0=默认不开启，1=开启
        :type UpdateProhibition: int
        :param _TransferProhibition: 是否开启转移锁：0=默认不开启，1=开启
        :type TransferProhibition: int
        :param _ChannelFrom: 渠道来源，pc/miniprogram/h5等
        :type ChannelFrom: str
        :param _OrderFrom: 订单来源，common正常/dianshi_active点石活动等
        :type OrderFrom: str
        :param _ActivityId: 活动id
        :type ActivityId: str
        """
        self._TemplateId = None
        self._Period = None
        self._Domains = None
        self._PayMode = None
        self._AutoRenewFlag = None
        self._PackageResourceId = None
        self._UpdateProhibition = None
        self._TransferProhibition = None
        self._ChannelFrom = None
        self._OrderFrom = None
        self._ActivityId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def PayMode(self):
        return self._PayMode

    @PayMode.setter
    def PayMode(self, PayMode):
        self._PayMode = PayMode

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def PackageResourceId(self):
        return self._PackageResourceId

    @PackageResourceId.setter
    def PackageResourceId(self, PackageResourceId):
        self._PackageResourceId = PackageResourceId

    @property
    def UpdateProhibition(self):
        return self._UpdateProhibition

    @UpdateProhibition.setter
    def UpdateProhibition(self, UpdateProhibition):
        self._UpdateProhibition = UpdateProhibition

    @property
    def TransferProhibition(self):
        return self._TransferProhibition

    @TransferProhibition.setter
    def TransferProhibition(self, TransferProhibition):
        self._TransferProhibition = TransferProhibition

    @property
    def ChannelFrom(self):
        return self._ChannelFrom

    @ChannelFrom.setter
    def ChannelFrom(self, ChannelFrom):
        self._ChannelFrom = ChannelFrom

    @property
    def OrderFrom(self):
        return self._OrderFrom

    @OrderFrom.setter
    def OrderFrom(self, OrderFrom):
        self._OrderFrom = OrderFrom

    @property
    def ActivityId(self):
        return self._ActivityId

    @ActivityId.setter
    def ActivityId(self, ActivityId):
        self._ActivityId = ActivityId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        self._Period = params.get("Period")
        self._Domains = params.get("Domains")
        self._PayMode = params.get("PayMode")
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._PackageResourceId = params.get("PackageResourceId")
        self._UpdateProhibition = params.get("UpdateProhibition")
        self._TransferProhibition = params.get("TransferProhibition")
        self._ChannelFrom = params.get("ChannelFrom")
        self._OrderFrom = params.get("OrderFrom")
        self._ActivityId = params.get("ActivityId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDomainBatchResponse(AbstractModel):
    """CreateDomainBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 批量日志ID
注意：此字段可能返回 null，表示取不到有效值。
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class CreateDomainRedemptionRequest(AbstractModel):
    """CreateDomainRedemption请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名 ID
        :type DomainId: str
        """
        self._DomainId = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDomainRedemptionResponse(AbstractModel):
    """CreateDomainRedemption返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreatePhoneEmailRequest(AbstractModel):
    """CreatePhoneEmail请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Code: 手机号或者邮箱
        :type Code: str
        :param _Type: 1：手机   2：邮箱
        :type Type: int
        :param _VerifyCode: 验证码
        :type VerifyCode: str
        """
        self._Code = None
        self._Type = None
        self._VerifyCode = None

    @property
    def Code(self):
        return self._Code

    @Code.setter
    def Code(self, Code):
        self._Code = Code

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def VerifyCode(self):
        return self._VerifyCode

    @VerifyCode.setter
    def VerifyCode(self, VerifyCode):
        self._VerifyCode = VerifyCode


    def _deserialize(self, params):
        self._Code = params.get("Code")
        self._Type = params.get("Type")
        self._VerifyCode = params.get("VerifyCode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePhoneEmailResponse(AbstractModel):
    """CreatePhoneEmail返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateTemplateRequest(AbstractModel):
    """CreateTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ContactInfo: 联系人信息
        :type ContactInfo: :class:`tencentcloud.domain.v20180808.models.ContactInfo`
        :param _CertificateInfo: 证件信息
        :type CertificateInfo: :class:`tencentcloud.domain.v20180808.models.CertificateInfo`
        """
        self._ContactInfo = None
        self._CertificateInfo = None

    @property
    def ContactInfo(self):
        return self._ContactInfo

    @ContactInfo.setter
    def ContactInfo(self, ContactInfo):
        self._ContactInfo = ContactInfo

    @property
    def CertificateInfo(self):
        return self._CertificateInfo

    @CertificateInfo.setter
    def CertificateInfo(self, CertificateInfo):
        self._CertificateInfo = CertificateInfo


    def _deserialize(self, params):
        if params.get("ContactInfo") is not None:
            self._ContactInfo = ContactInfo()
            self._ContactInfo._deserialize(params.get("ContactInfo"))
        if params.get("CertificateInfo") is not None:
            self._CertificateInfo = CertificateInfo()
            self._CertificateInfo._deserialize(params.get("CertificateInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTemplateResponse(AbstractModel):
    """CreateTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Template: 模板信息
        :type Template: :class:`tencentcloud.domain.v20180808.models.TemplateInfo`
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Template = None
        self._RequestId = None

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Template") is not None:
            self._Template = TemplateInfo()
            self._Template._deserialize(params.get("Template"))
        self._RequestId = params.get("RequestId")


class CustomDnsHost(AbstractModel):
    """自定义DNS Host

    """

    def __init__(self):
        r"""
        :param _DnsName: DNS名称
        :type DnsName: str
        :param _IpSet: IP地址列表
        :type IpSet: list of str
        """
        self._DnsName = None
        self._IpSet = None

    @property
    def DnsName(self):
        return self._DnsName

    @DnsName.setter
    def DnsName(self, DnsName):
        self._DnsName = DnsName

    @property
    def IpSet(self):
        return self._IpSet

    @IpSet.setter
    def IpSet(self, IpSet):
        self._IpSet = IpSet


    def _deserialize(self, params):
        self._DnsName = params.get("DnsName")
        self._IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCustomDnsHostRequest(AbstractModel):
    """DeleteCustomDnsHost请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名实例ID
        :type DomainId: str
        :param _DnsName: DNS名称
        :type DnsName: str
        """
        self._DomainId = None
        self._DnsName = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DnsName(self):
        return self._DnsName

    @DnsName.setter
    def DnsName(self, DnsName):
        self._DnsName = DnsName


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DnsName = params.get("DnsName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCustomDnsHostResponse(AbstractModel):
    """DeleteCustomDnsHost返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 异步任务ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class DeletePhoneEmailRequest(AbstractModel):
    """DeletePhoneEmail请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Code: 手机或者邮箱
        :type Code: str
        :param _Type: 1：手机  2：邮箱
        :type Type: int
        """
        self._Code = None
        self._Type = None

    @property
    def Code(self):
        return self._Code

    @Code.setter
    def Code(self, Code):
        self._Code = Code

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type


    def _deserialize(self, params):
        self._Code = params.get("Code")
        self._Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePhoneEmailResponse(AbstractModel):
    """DeletePhoneEmail返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteReservedPreDomainInfoRequest(AbstractModel):
    """DeleteReservedPreDomainInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ResourceIdList: 资源ID列表
        :type ResourceIdList: list of str
        """
        self._ResourceIdList = None

    @property
    def ResourceIdList(self):
        return self._ResourceIdList

    @ResourceIdList.setter
    def ResourceIdList(self, ResourceIdList):
        self._ResourceIdList = ResourceIdList


    def _deserialize(self, params):
        self._ResourceIdList = params.get("ResourceIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteReservedPreDomainInfoResponse(AbstractModel):
    """DeleteReservedPreDomainInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteTemplateRequest(AbstractModel):
    """DeleteTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTemplateResponse(AbstractModel):
    """DeleteTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DescribeBatchOperationLogDetailsRequest(AbstractModel):
    """DescribeBatchOperationLogDetails请求参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID。
        :type LogId: int
        :param _Offset: 偏移量，默认为0。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为200。
        :type Limit: int
        """
        self._LogId = None
        self._Offset = None
        self._Limit = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBatchOperationLogDetailsResponse(AbstractModel):
    """DescribeBatchOperationLogDetails返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 总数量。
        :type TotalCount: int
        :param _DomainBatchDetailSet: 日志详情列表。
注意：此字段可能返回 null，表示取不到有效值。
        :type DomainBatchDetailSet: list of DomainBatchDetailSet
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._DomainBatchDetailSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def DomainBatchDetailSet(self):
        return self._DomainBatchDetailSet

    @DomainBatchDetailSet.setter
    def DomainBatchDetailSet(self, DomainBatchDetailSet):
        self._DomainBatchDetailSet = DomainBatchDetailSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("DomainBatchDetailSet") is not None:
            self._DomainBatchDetailSet = []
            for item in params.get("DomainBatchDetailSet"):
                obj = DomainBatchDetailSet()
                obj._deserialize(item)
                self._DomainBatchDetailSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeBatchOperationLogsRequest(AbstractModel):
    """DescribeBatchOperationLogs请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Offset: 偏移量，默认为0。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为200。
        :type Limit: int
        """
        self._Offset = None
        self._Limit = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBatchOperationLogsResponse(AbstractModel):
    """DescribeBatchOperationLogs返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 总数量
        :type TotalCount: int
        :param _DomainBatchLogSet: 日志列表
注意：此字段可能返回 null，表示取不到有效值。
        :type DomainBatchLogSet: list of DomainBatchLogSet
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._DomainBatchLogSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def DomainBatchLogSet(self):
        return self._DomainBatchLogSet

    @DomainBatchLogSet.setter
    def DomainBatchLogSet(self, DomainBatchLogSet):
        self._DomainBatchLogSet = DomainBatchLogSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("DomainBatchLogSet") is not None:
            self._DomainBatchLogSet = []
            for item in params.get("DomainBatchLogSet"):
                obj = DomainBatchLogSet()
                obj._deserialize(item)
                self._DomainBatchLogSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeCustomDnsHostSetRequest(AbstractModel):
    """DescribeCustomDnsHostSet请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名实例ID
        :type DomainId: str
        :param _Limit: 返回数量，默认为20，取值范围[1,100]
        :type Limit: int
        :param _Offset: 偏移量，默认为0
        :type Offset: int
        """
        self._DomainId = None
        self._Limit = None
        self._Offset = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCustomDnsHostSetResponse(AbstractModel):
    """DescribeCustomDnsHostSet返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DnsHostSet: 自定义DNS Host 列表
注意：此字段可能返回 null，表示取不到有效值。
        :type DnsHostSet: list of CustomDnsHost
        :param _TotalCount: 自定义DNS Host总数
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DnsHostSet = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def DnsHostSet(self):
        return self._DnsHostSet

    @DnsHostSet.setter
    def DnsHostSet(self, DnsHostSet):
        self._DnsHostSet = DnsHostSet

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("DnsHostSet") is not None:
            self._DnsHostSet = []
            for item in params.get("DnsHostSet"):
                obj = CustomDnsHost()
                obj._deserialize(item)
                self._DnsHostSet.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeDomainBaseInfoRequest(AbstractModel):
    """DescribeDomainBaseInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domain: 域名
        :type Domain: str
        """
        self._Domain = None

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain


    def _deserialize(self, params):
        self._Domain = params.get("Domain")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDomainBaseInfoResponse(AbstractModel):
    """DescribeDomainBaseInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainInfo: 域名信息
        :type DomainInfo: :class:`tencentcloud.domain.v20180808.models.DomainBaseInfo`
        :param _Uin: 用户Uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DomainInfo = None
        self._Uin = None
        self._RequestId = None

    @property
    def DomainInfo(self):
        return self._DomainInfo

    @DomainInfo.setter
    def DomainInfo(self, DomainInfo):
        self._DomainInfo = DomainInfo

    @property
    def Uin(self):
        return self._Uin

    @Uin.setter
    def Uin(self, Uin):
        self._Uin = Uin

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("DomainInfo") is not None:
            self._DomainInfo = DomainBaseInfo()
            self._DomainInfo._deserialize(params.get("DomainInfo"))
        self._Uin = params.get("Uin")
        self._RequestId = params.get("RequestId")


class DescribeDomainNameListRequest(AbstractModel):
    """DescribeDomainNameList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Offset: 偏移量，默认为0
        :type Offset: int
        :param _Limit: 返回数量，默认为20，取值范围[1,100]
        :type Limit: int
        """
        self._Offset = None
        self._Limit = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDomainNameListResponse(AbstractModel):
    """DescribeDomainNameList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainSet: 域名信息集合
注意：此字段可能返回 null，表示取不到有效值。
        :type DomainSet: list of DomainList
        :param _TotalCount: 域名总数量
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DomainSet = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def DomainSet(self):
        return self._DomainSet

    @DomainSet.setter
    def DomainSet(self, DomainSet):
        self._DomainSet = DomainSet

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("DomainSet") is not None:
            self._DomainSet = []
            for item in params.get("DomainSet"):
                obj = DomainList()
                obj._deserialize(item)
                self._DomainSet.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribeDomainPriceListRequest(AbstractModel):
    """DescribeDomainPriceList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TldList: 查询价格的后缀列表。默认则为全部后缀
        :type TldList: list of str
        :param _Year: 查询购买的年份，默认会列出所有年份的价格
        :type Year: list of int
        :param _Operation: 域名的购买类型：new  新购，renew 续费，redem 赎回，tran 转入
        :type Operation: list of str
        """
        self._TldList = None
        self._Year = None
        self._Operation = None

    @property
    def TldList(self):
        return self._TldList

    @TldList.setter
    def TldList(self, TldList):
        self._TldList = TldList

    @property
    def Year(self):
        return self._Year

    @Year.setter
    def Year(self, Year):
        self._Year = Year

    @property
    def Operation(self):
        return self._Operation

    @Operation.setter
    def Operation(self, Operation):
        self._Operation = Operation


    def _deserialize(self, params):
        self._TldList = params.get("TldList")
        self._Year = params.get("Year")
        self._Operation = params.get("Operation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDomainPriceListResponse(AbstractModel):
    """DescribeDomainPriceList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _PriceList: 域名价格列表
        :type PriceList: list of PriceInfo
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._PriceList = None
        self._RequestId = None

    @property
    def PriceList(self):
        return self._PriceList

    @PriceList.setter
    def PriceList(self, PriceList):
        self._PriceList = PriceList

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("PriceList") is not None:
            self._PriceList = []
            for item in params.get("PriceList"):
                obj = PriceInfo()
                obj._deserialize(item)
                self._PriceList.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeDomainSimpleInfoRequest(AbstractModel):
    """DescribeDomainSimpleInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainName: 域名
        :type DomainName: str
        """
        self._DomainName = None

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName


    def _deserialize(self, params):
        self._DomainName = params.get("DomainName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDomainSimpleInfoResponse(AbstractModel):
    """DescribeDomainSimpleInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainInfo: 域名信息
        :type DomainInfo: :class:`tencentcloud.domain.v20180808.models.DomainSimpleInfo`
        :param _Uin: 账号ID
        :type Uin: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._DomainInfo = None
        self._Uin = None
        self._RequestId = None

    @property
    def DomainInfo(self):
        return self._DomainInfo

    @DomainInfo.setter
    def DomainInfo(self, DomainInfo):
        self._DomainInfo = DomainInfo

    @property
    def Uin(self):
        return self._Uin

    @Uin.setter
    def Uin(self, Uin):
        self._Uin = Uin

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("DomainInfo") is not None:
            self._DomainInfo = DomainSimpleInfo()
            self._DomainInfo._deserialize(params.get("DomainInfo"))
        self._Uin = params.get("Uin")
        self._RequestId = params.get("RequestId")


class DescribePhoneEmailListRequest(AbstractModel):
    """DescribePhoneEmailList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Type: 0：所有类型  1：手机  2：邮箱，默认0
        :type Type: int
        :param _Offset: 偏移量，默认为0
        :type Offset: int
        :param _Limit: 返回数量，默认为20，取值范围[1,200]
        :type Limit: int
        :param _Code: 手机或者邮箱，用于精确搜索
        :type Code: str
        """
        self._Type = None
        self._Offset = None
        self._Limit = None
        self._Code = None

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Code(self):
        return self._Code

    @Code.setter
    def Code(self, Code):
        self._Code = Code


    def _deserialize(self, params):
        self._Type = params.get("Type")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._Code = params.get("Code")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePhoneEmailListResponse(AbstractModel):
    """DescribePhoneEmailList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _PhoneEmailList: 手机或者邮箱列表
        :type PhoneEmailList: list of PhoneEmailData
        :param _TotalCount: 总数量。
        :type TotalCount: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._PhoneEmailList = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def PhoneEmailList(self):
        return self._PhoneEmailList

    @PhoneEmailList.setter
    def PhoneEmailList(self, PhoneEmailList):
        self._PhoneEmailList = PhoneEmailList

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("PhoneEmailList") is not None:
            self._PhoneEmailList = []
            for item in params.get("PhoneEmailList"):
                obj = PhoneEmailData()
                obj._deserialize(item)
                self._PhoneEmailList.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class DescribePreDomainListRequest(AbstractModel):
    """DescribePreDomainList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Page: 页码
        :type Page: int
        :param _Size: 条数
        :type Size: int
        :param _EndTime: 用于结束时间筛选
        :type EndTime: str
        :param _UpTime: 用户指定上架时间筛选
        :type UpTime: str
        """
        self._Page = None
        self._Size = None
        self._EndTime = None
        self._UpTime = None

    @property
    def Page(self):
        return self._Page

    @Page.setter
    def Page(self, Page):
        self._Page = Page

    @property
    def Size(self):
        return self._Size

    @Size.setter
    def Size(self, Size):
        self._Size = Size

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def UpTime(self):
        return self._UpTime

    @UpTime.setter
    def UpTime(self, UpTime):
        self._UpTime = UpTime


    def _deserialize(self, params):
        self._Page = params.get("Page")
        self._Size = params.get("Size")
        self._EndTime = params.get("EndTime")
        self._UpTime = params.get("UpTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePreDomainListResponse(AbstractModel):
    """DescribePreDomainList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ReservedDomainList: 预释放预约列表数据
        :type ReservedDomainList: list of ReservedDomainInfo
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ReservedDomainList = None
        self._Total = None
        self._RequestId = None

    @property
    def ReservedDomainList(self):
        return self._ReservedDomainList

    @ReservedDomainList.setter
    def ReservedDomainList(self, ReservedDomainList):
        self._ReservedDomainList = ReservedDomainList

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ReservedDomainList") is not None:
            self._ReservedDomainList = []
            for item in params.get("ReservedDomainList"):
                obj = ReservedDomainInfo()
                obj._deserialize(item)
                self._ReservedDomainList.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeReservedPreDomainInfoRequest(AbstractModel):
    """DescribeReservedPreDomainInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainList: 域名,每次最多支持500条域名查询
        :type DomainList: list of str
        :param _ReservedStatus: 状态，用于筛选，可不填写(1. 预定成功 2. 预定失败（预定失败Reason字段将会被赋值）3. 域名交割中 4. 域名交割完成)
        :type ReservedStatus: int
        :param _ReservedTimeSort: 根据预约时间排序，仅支持："desc","asc"。
        :type ReservedTimeSort: str
        :param _Limit: 条数
        :type Limit: int
        :param _Offset: 偏移量
        :type Offset: int
        """
        self._DomainList = None
        self._ReservedStatus = None
        self._ReservedTimeSort = None
        self._Limit = None
        self._Offset = None

    @property
    def DomainList(self):
        return self._DomainList

    @DomainList.setter
    def DomainList(self, DomainList):
        self._DomainList = DomainList

    @property
    def ReservedStatus(self):
        return self._ReservedStatus

    @ReservedStatus.setter
    def ReservedStatus(self, ReservedStatus):
        self._ReservedStatus = ReservedStatus

    @property
    def ReservedTimeSort(self):
        return self._ReservedTimeSort

    @ReservedTimeSort.setter
    def ReservedTimeSort(self, ReservedTimeSort):
        self._ReservedTimeSort = ReservedTimeSort

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset


    def _deserialize(self, params):
        self._DomainList = params.get("DomainList")
        self._ReservedStatus = params.get("ReservedStatus")
        self._ReservedTimeSort = params.get("ReservedTimeSort")
        self._Limit = params.get("Limit")
        self._Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeReservedPreDomainInfoResponse(AbstractModel):
    """DescribeReservedPreDomainInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param _ReservedPreDomainInfoList: 预释放预约列表
        :type ReservedPreDomainInfoList: list of ReservedPreDomainInfo
        :param _Total: 总数
        :type Total: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._ReservedPreDomainInfoList = None
        self._Total = None
        self._RequestId = None

    @property
    def ReservedPreDomainInfoList(self):
        return self._ReservedPreDomainInfoList

    @ReservedPreDomainInfoList.setter
    def ReservedPreDomainInfoList(self, ReservedPreDomainInfoList):
        self._ReservedPreDomainInfoList = ReservedPreDomainInfoList

    @property
    def Total(self):
        return self._Total

    @Total.setter
    def Total(self, Total):
        self._Total = Total

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("ReservedPreDomainInfoList") is not None:
            self._ReservedPreDomainInfoList = []
            for item in params.get("ReservedPreDomainInfoList"):
                obj = ReservedPreDomainInfo()
                obj._deserialize(item)
                self._ReservedPreDomainInfoList.append(obj)
        self._Total = params.get("Total")
        self._RequestId = params.get("RequestId")


class DescribeTemplateListRequest(AbstractModel):
    """DescribeTemplateList请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Offset: 偏移量，默认为0。
        :type Offset: int
        :param _Limit: 返回数量，默认为20，最大值为100。
        :type Limit: int
        :param _Type: 用户注册类型，默认:all , 个人：I ,企业: E
        :type Type: str
        :param _Status: 认证状态：未实名审核:NotUpload, 实名审核中:InAudit，已实名审核:Approved，实名审核失败:Reject，更新手机邮箱:NotVerified。
        :type Status: str
        :param _Keyword: 关键字，用于域名所有者筛选
        :type Keyword: str
        """
        self._Offset = None
        self._Limit = None
        self._Type = None
        self._Status = None
        self._Keyword = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Keyword(self):
        return self._Keyword

    @Keyword.setter
    def Keyword(self, Keyword):
        self._Keyword = Keyword


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        self._Type = params.get("Type")
        self._Status = params.get("Status")
        self._Keyword = params.get("Keyword")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTemplateListResponse(AbstractModel):
    """DescribeTemplateList返回参数结构体

    """

    def __init__(self):
        r"""
        :param _TotalCount: 模板数量。
        :type TotalCount: int
        :param _TemplateSet: 模板详细信息列表。
        :type TemplateSet: list of TemplateInfo
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._TotalCount = None
        self._TemplateSet = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def TemplateSet(self):
        return self._TemplateSet

    @TemplateSet.setter
    def TemplateSet(self, TemplateSet):
        self._TemplateSet = TemplateSet

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("TemplateSet") is not None:
            self._TemplateSet = []
            for item in params.get("TemplateSet"):
                obj = TemplateInfo()
                obj._deserialize(item)
                self._TemplateSet.append(obj)
        self._RequestId = params.get("RequestId")


class DescribeTemplateRequest(AbstractModel):
    """DescribeTemplate请求参数结构体

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        """
        self._TemplateId = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTemplateResponse(AbstractModel):
    """DescribeTemplate返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Template: 模板信息
        :type Template: :class:`tencentcloud.domain.v20180808.models.TemplateInfo`
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Template = None
        self._RequestId = None

    @property
    def Template(self):
        return self._Template

    @Template.setter
    def Template(self, Template):
        self._Template = Template

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Template") is not None:
            self._Template = TemplateInfo()
            self._Template._deserialize(params.get("Template"))
        self._RequestId = params.get("RequestId")


class DomainBaseInfo(AbstractModel):
    """获取域名基础信息

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名资源ID。
        :type DomainId: str
        :param _DomainName: 域名名称。
        :type DomainName: str
        :param _RealNameAuditStatus: 域名实名认证状态。
NotUpload：未实名认证
InAudit：实名审核中
Approved：实名审核通过
Reject：实名审核失败
NoAudit: 无需实名认证
        :type RealNameAuditStatus: str
        :param _RealNameAuditUnpassReason: 域名实名认证不通过原因。
注意：此字段可能返回 null，表示取不到有效值。
        :type RealNameAuditUnpassReason: str
        :param _DomainNameAuditStatus: 域名命名审核状态。
NotAudit：命名审核未上传
Pending：命名审核待上传
Auditing：域名命名审核中
Approved：域名命名审核通过
Rejected：域名命名审核拒绝
        :type DomainNameAuditStatus: str
        :param _DomainNameAuditUnpassReason: 域名命名审核不通过原因。
注意：此字段可能返回 null，表示取不到有效值。
        :type DomainNameAuditUnpassReason: str
        :param _CreationDate: 注册时间。
        :type CreationDate: str
        :param _ExpirationDate: 到期时间
        :type ExpirationDate: str
        :param _DomainStatus: 域名状态。
ok：正常
serverHold：注册局暂停解析 
clientHold：注册商暂停解析
pendingTransfer：转移中
renewingPeriod：续费期
redemptionPeriod：偿还期
pendingDelete：删除期
serverTransferProhibited：注册局禁止转移
serverUpdateProhibited：注册局禁止更新
serverDeleteProhibited：注册局禁止删除
clientTransferProhibited：注册商禁止转移
clientUpdateProhibited：注册商禁止更新
clientDeleteProhibited：注册商禁止删除
serverRenewProhibited: 注册局禁止续费
clientRenewProhobited: 注册商禁止续费
        :type DomainStatus: list of str
        :param _BuyStatus: 域名购买状态。
ok：正常
RegisterPending：待注册
RegisterDoing：注册中
RegisterFailed：注册失败
AboutToExpire: 即将过期
RenewPending：已进入续费期，需要进行续费
RenewDoing：续费中
RedemptionPending：已进入赎回期，需要进行续费
RedemptionDoing：赎回中
TransferPending：待转入中
TransferTransing：转入中
TransferFailed：转入失败
        :type BuyStatus: str
        :param _RegistrarType: 注册商类型
epp: DNSPod, Inc.（烟台帝思普网络科技有限公司）
qcloud: Tencent Cloud Computing (Beijing) Limited Liability Company（腾讯云计算（北京）有限责任公司）
yunxun: Guangzhou Yunxun Information Technology Co., Ltd.（广州云讯信息科技有限公司）
xinnet: Xin Net Technology Corporation（北京新网数码信息技术有限公司）
        :type RegistrarType: str
        :param _NameServer: 域名绑定的ns
        :type NameServer: list of str
        :param _LockTransfer: true：开启锁定
false：关闭锁定
        :type LockTransfer: bool
        :param _LockEndTime: 锁定结束时间
        :type LockEndTime: str
        """
        self._DomainId = None
        self._DomainName = None
        self._RealNameAuditStatus = None
        self._RealNameAuditUnpassReason = None
        self._DomainNameAuditStatus = None
        self._DomainNameAuditUnpassReason = None
        self._CreationDate = None
        self._ExpirationDate = None
        self._DomainStatus = None
        self._BuyStatus = None
        self._RegistrarType = None
        self._NameServer = None
        self._LockTransfer = None
        self._LockEndTime = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName

    @property
    def RealNameAuditStatus(self):
        return self._RealNameAuditStatus

    @RealNameAuditStatus.setter
    def RealNameAuditStatus(self, RealNameAuditStatus):
        self._RealNameAuditStatus = RealNameAuditStatus

    @property
    def RealNameAuditUnpassReason(self):
        return self._RealNameAuditUnpassReason

    @RealNameAuditUnpassReason.setter
    def RealNameAuditUnpassReason(self, RealNameAuditUnpassReason):
        self._RealNameAuditUnpassReason = RealNameAuditUnpassReason

    @property
    def DomainNameAuditStatus(self):
        return self._DomainNameAuditStatus

    @DomainNameAuditStatus.setter
    def DomainNameAuditStatus(self, DomainNameAuditStatus):
        self._DomainNameAuditStatus = DomainNameAuditStatus

    @property
    def DomainNameAuditUnpassReason(self):
        return self._DomainNameAuditUnpassReason

    @DomainNameAuditUnpassReason.setter
    def DomainNameAuditUnpassReason(self, DomainNameAuditUnpassReason):
        self._DomainNameAuditUnpassReason = DomainNameAuditUnpassReason

    @property
    def CreationDate(self):
        return self._CreationDate

    @CreationDate.setter
    def CreationDate(self, CreationDate):
        self._CreationDate = CreationDate

    @property
    def ExpirationDate(self):
        return self._ExpirationDate

    @ExpirationDate.setter
    def ExpirationDate(self, ExpirationDate):
        self._ExpirationDate = ExpirationDate

    @property
    def DomainStatus(self):
        return self._DomainStatus

    @DomainStatus.setter
    def DomainStatus(self, DomainStatus):
        self._DomainStatus = DomainStatus

    @property
    def BuyStatus(self):
        return self._BuyStatus

    @BuyStatus.setter
    def BuyStatus(self, BuyStatus):
        self._BuyStatus = BuyStatus

    @property
    def RegistrarType(self):
        return self._RegistrarType

    @RegistrarType.setter
    def RegistrarType(self, RegistrarType):
        self._RegistrarType = RegistrarType

    @property
    def NameServer(self):
        return self._NameServer

    @NameServer.setter
    def NameServer(self, NameServer):
        self._NameServer = NameServer

    @property
    def LockTransfer(self):
        return self._LockTransfer

    @LockTransfer.setter
    def LockTransfer(self, LockTransfer):
        self._LockTransfer = LockTransfer

    @property
    def LockEndTime(self):
        return self._LockEndTime

    @LockEndTime.setter
    def LockEndTime(self, LockEndTime):
        self._LockEndTime = LockEndTime


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DomainName = params.get("DomainName")
        self._RealNameAuditStatus = params.get("RealNameAuditStatus")
        self._RealNameAuditUnpassReason = params.get("RealNameAuditUnpassReason")
        self._DomainNameAuditStatus = params.get("DomainNameAuditStatus")
        self._DomainNameAuditUnpassReason = params.get("DomainNameAuditUnpassReason")
        self._CreationDate = params.get("CreationDate")
        self._ExpirationDate = params.get("ExpirationDate")
        self._DomainStatus = params.get("DomainStatus")
        self._BuyStatus = params.get("BuyStatus")
        self._RegistrarType = params.get("RegistrarType")
        self._NameServer = params.get("NameServer")
        self._LockTransfer = params.get("LockTransfer")
        self._LockEndTime = params.get("LockEndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DomainBatchDetailSet(AbstractModel):
    """批量操作日志详情

    """

    def __init__(self):
        r"""
        :param _Id: 详情ID
        :type Id: int
        :param _Action: 类型  new: 注册域名 batch_transfer_prohibition_on:开启禁止转移  batch_transfer_prohibition_off:关闭禁止转移 batch_update_prohibition_on:开启禁止更新   batch_update_prohibition_off:关闭禁止更新
        :type Action: str
        :param _Domain: 域名
        :type Domain: str
        :param _Status: 执行状态：
doing 执行中。
failed 操作失败。
success  操作成功。
        :type Status: str
        :param _Reason: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param _CreatedOn: 创建时间
        :type CreatedOn: str
        :param _UpdatedOn: 更新时间
        :type UpdatedOn: str
        :param _BigDealId: 订单号
注意：此字段可能返回 null，表示取不到有效值。
        :type BigDealId: str
        """
        self._Id = None
        self._Action = None
        self._Domain = None
        self._Status = None
        self._Reason = None
        self._CreatedOn = None
        self._UpdatedOn = None
        self._BigDealId = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def Action(self):
        return self._Action

    @Action.setter
    def Action(self, Action):
        self._Action = Action

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Reason(self):
        return self._Reason

    @Reason.setter
    def Reason(self, Reason):
        self._Reason = Reason

    @property
    def CreatedOn(self):
        return self._CreatedOn

    @CreatedOn.setter
    def CreatedOn(self, CreatedOn):
        self._CreatedOn = CreatedOn

    @property
    def UpdatedOn(self):
        return self._UpdatedOn

    @UpdatedOn.setter
    def UpdatedOn(self, UpdatedOn):
        self._UpdatedOn = UpdatedOn

    @property
    def BigDealId(self):
        return self._BigDealId

    @BigDealId.setter
    def BigDealId(self, BigDealId):
        self._BigDealId = BigDealId


    def _deserialize(self, params):
        self._Id = params.get("Id")
        self._Action = params.get("Action")
        self._Domain = params.get("Domain")
        self._Status = params.get("Status")
        self._Reason = params.get("Reason")
        self._CreatedOn = params.get("CreatedOn")
        self._UpdatedOn = params.get("UpdatedOn")
        self._BigDealId = params.get("BigDealId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DomainBatchLogSet(AbstractModel):
    """批量操作记录

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID
        :type LogId: int
        :param _Number: 数量
        :type Number: int
        :param _Status: 执行状态：
doing 执行中。
done 执行完成。
        :type Status: str
        :param _CreatedOn: 提交时间
        :type CreatedOn: str
        :param _Success: 批量操作成功个数
        :type Success: int
        :param _Doing: 批量操作处理中个数
        :type Doing: int
        :param _Failed: 批量操作失败个数
        :type Failed: int
        """
        self._LogId = None
        self._Number = None
        self._Status = None
        self._CreatedOn = None
        self._Success = None
        self._Doing = None
        self._Failed = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def Number(self):
        return self._Number

    @Number.setter
    def Number(self, Number):
        self._Number = Number

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def CreatedOn(self):
        return self._CreatedOn

    @CreatedOn.setter
    def CreatedOn(self, CreatedOn):
        self._CreatedOn = CreatedOn

    @property
    def Success(self):
        return self._Success

    @Success.setter
    def Success(self, Success):
        self._Success = Success

    @property
    def Doing(self):
        return self._Doing

    @Doing.setter
    def Doing(self, Doing):
        self._Doing = Doing

    @property
    def Failed(self):
        return self._Failed

    @Failed.setter
    def Failed(self, Failed):
        self._Failed = Failed


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._Number = params.get("Number")
        self._Status = params.get("Status")
        self._CreatedOn = params.get("CreatedOn")
        self._Success = params.get("Success")
        self._Doing = params.get("Doing")
        self._Failed = params.get("Failed")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DomainList(AbstractModel):
    """域名列表

    """

    def __init__(self):
        r"""
        :param _IsPremium: 是否是溢价域名：
ture 是    
false 不是
        :type IsPremium: bool
        :param _DomainId: 域名资源ID。
        :type DomainId: str
        :param _DomainName: 域名名称。
        :type DomainName: str
        :param _AutoRenew: 是否已设置自动续费 。
0：未设置 
1：已设置
2：设置后，关闭
        :type AutoRenew: int
        :param _CreationDate: 注册时间。
        :type CreationDate: str
        :param _ExpirationDate: 到期时间。
        :type ExpirationDate: str
        :param _Tld: 域名后缀
        :type Tld: str
        :param _CodeTld: 编码后的后缀（中文会进行编码）
        :type CodeTld: str
        :param _BuyStatus: 域名购买状态。
ok：正常
AboutToExpire: 即将到期
RegisterPending：注册中
RegisterDoing：注册中
RegisterFailed：注册失败
RenewPending：续费期
RenewDoing：续费中
RedemptionPending：赎回期
RedemptionDoing：赎回中
TransferPending：转入中
TransferTransing：转入中
TransferFailed：转入失败
        :type BuyStatus: str
        """
        self._IsPremium = None
        self._DomainId = None
        self._DomainName = None
        self._AutoRenew = None
        self._CreationDate = None
        self._ExpirationDate = None
        self._Tld = None
        self._CodeTld = None
        self._BuyStatus = None

    @property
    def IsPremium(self):
        return self._IsPremium

    @IsPremium.setter
    def IsPremium(self, IsPremium):
        self._IsPremium = IsPremium

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName

    @property
    def AutoRenew(self):
        return self._AutoRenew

    @AutoRenew.setter
    def AutoRenew(self, AutoRenew):
        self._AutoRenew = AutoRenew

    @property
    def CreationDate(self):
        return self._CreationDate

    @CreationDate.setter
    def CreationDate(self, CreationDate):
        self._CreationDate = CreationDate

    @property
    def ExpirationDate(self):
        return self._ExpirationDate

    @ExpirationDate.setter
    def ExpirationDate(self, ExpirationDate):
        self._ExpirationDate = ExpirationDate

    @property
    def Tld(self):
        return self._Tld

    @Tld.setter
    def Tld(self, Tld):
        self._Tld = Tld

    @property
    def CodeTld(self):
        return self._CodeTld

    @CodeTld.setter
    def CodeTld(self, CodeTld):
        self._CodeTld = CodeTld

    @property
    def BuyStatus(self):
        return self._BuyStatus

    @BuyStatus.setter
    def BuyStatus(self, BuyStatus):
        self._BuyStatus = BuyStatus


    def _deserialize(self, params):
        self._IsPremium = params.get("IsPremium")
        self._DomainId = params.get("DomainId")
        self._DomainName = params.get("DomainName")
        self._AutoRenew = params.get("AutoRenew")
        self._CreationDate = params.get("CreationDate")
        self._ExpirationDate = params.get("ExpirationDate")
        self._Tld = params.get("Tld")
        self._CodeTld = params.get("CodeTld")
        self._BuyStatus = params.get("BuyStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DomainSimpleInfo(AbstractModel):
    """获取域名基础模板信息

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名资源ID。
        :type DomainId: str
        :param _DomainName: 域名名称。
        :type DomainName: str
        :param _RealNameAuditStatus: 域名实名认证状态。
NotUpload：未实名认证
InAudit：实名审核中
Approved：实名审核通过
Reject：实名审核失败
NoAudit: 无需实名认证
        :type RealNameAuditStatus: str
        :param _RealNameAuditUnpassReason: 域名实名认证不通过原因。
注意：此字段可能返回 null，表示取不到有效值。
        :type RealNameAuditUnpassReason: str
        :param _DomainNameAuditStatus: 域名命名审核状态。
NotAudit：命名审核未上传
Pending：命名审核待上传
Auditing：域名命名审核中
Approved：域名命名审核通过
Rejected：域名命名审核拒绝
        :type DomainNameAuditStatus: str
        :param _DomainNameAuditUnpassReason: 域名命名审核不通过原因。
注意：此字段可能返回 null，表示取不到有效值。
        :type DomainNameAuditUnpassReason: str
        :param _CreationDate: 注册时间。
        :type CreationDate: str
        :param _ExpirationDate: 到期时间
        :type ExpirationDate: str
        :param _DomainStatus: 域名状态。
ok：正常
serverHold：注册局暂停解析 
clientHold：注册商暂停解析
pendingTransfer：转移中
renewingPeriod：续费期
redemptionPeriod：偿还期
pendingDelete：删除期
serverTransferProhibited：注册局禁止转移
serverUpdateProhibited：注册局禁止更新
serverDeleteProhibited：注册局禁止删除
clientTransferProhibited：注册商禁止转移
clientUpdateProhibited：注册商禁止更新
clientDeleteProhibited：注册商禁止删除
serverRenewProhibited: 注册局禁止续费
clientRenewProhobited: 注册商禁止续费
        :type DomainStatus: list of str
        :param _BuyStatus: 域名购买状态。
ok：正常
RegisterPending：待注册
RegisterDoing：注册中
RegisterFailed：注册失败
AboutToExpire: 即将过期
RenewPending：已进入续费期，需要进行续费
RenewDoing：续费中
RedemptionPending：已进入赎回期，需要进行续费
RedemptionDoing：赎回中
TransferPending：待转入中
TransferTransing：转入中
TransferFailed：转入失败
        :type BuyStatus: str
        :param _RegistrarType: 注册商类型
epp: DNSPod, Inc.（烟台帝思普网络科技有限公司）
qcloud: Tencent Cloud Computing (Beijing) Limited Liability Company（腾讯云计算（北京）有限责任公司）
yunxun: Guangzhou Yunxun Information Technology Co., Ltd.（广州云讯信息科技有限公司）
xinnet: Xin Net Technology Corporation（北京新网数码信息技术有限公司）
        :type RegistrarType: str
        :param _NameServer: 域名绑定的ns
        :type NameServer: list of str
        :param _LockTransfer: true：开启锁定
false：关闭锁定
        :type LockTransfer: bool
        :param _LockEndTime: 锁定结束时间
        :type LockEndTime: str
        :param _RegistrantType: 认证类型：I=个人，E=企业
        :type RegistrantType: str
        :param _OrganizationNameCN: 域名所有者，中文
        :type OrganizationNameCN: str
        :param _OrganizationName: 域名所有者，英文
        :type OrganizationName: str
        :param _RegistrantNameCN: 域名联系人，中文
        :type RegistrantNameCN: str
        :param _RegistrantName: 域名联系人，英文
        :type RegistrantName: str
        """
        self._DomainId = None
        self._DomainName = None
        self._RealNameAuditStatus = None
        self._RealNameAuditUnpassReason = None
        self._DomainNameAuditStatus = None
        self._DomainNameAuditUnpassReason = None
        self._CreationDate = None
        self._ExpirationDate = None
        self._DomainStatus = None
        self._BuyStatus = None
        self._RegistrarType = None
        self._NameServer = None
        self._LockTransfer = None
        self._LockEndTime = None
        self._RegistrantType = None
        self._OrganizationNameCN = None
        self._OrganizationName = None
        self._RegistrantNameCN = None
        self._RegistrantName = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DomainName(self):
        return self._DomainName

    @DomainName.setter
    def DomainName(self, DomainName):
        self._DomainName = DomainName

    @property
    def RealNameAuditStatus(self):
        return self._RealNameAuditStatus

    @RealNameAuditStatus.setter
    def RealNameAuditStatus(self, RealNameAuditStatus):
        self._RealNameAuditStatus = RealNameAuditStatus

    @property
    def RealNameAuditUnpassReason(self):
        return self._RealNameAuditUnpassReason

    @RealNameAuditUnpassReason.setter
    def RealNameAuditUnpassReason(self, RealNameAuditUnpassReason):
        self._RealNameAuditUnpassReason = RealNameAuditUnpassReason

    @property
    def DomainNameAuditStatus(self):
        return self._DomainNameAuditStatus

    @DomainNameAuditStatus.setter
    def DomainNameAuditStatus(self, DomainNameAuditStatus):
        self._DomainNameAuditStatus = DomainNameAuditStatus

    @property
    def DomainNameAuditUnpassReason(self):
        return self._DomainNameAuditUnpassReason

    @DomainNameAuditUnpassReason.setter
    def DomainNameAuditUnpassReason(self, DomainNameAuditUnpassReason):
        self._DomainNameAuditUnpassReason = DomainNameAuditUnpassReason

    @property
    def CreationDate(self):
        return self._CreationDate

    @CreationDate.setter
    def CreationDate(self, CreationDate):
        self._CreationDate = CreationDate

    @property
    def ExpirationDate(self):
        return self._ExpirationDate

    @ExpirationDate.setter
    def ExpirationDate(self, ExpirationDate):
        self._ExpirationDate = ExpirationDate

    @property
    def DomainStatus(self):
        return self._DomainStatus

    @DomainStatus.setter
    def DomainStatus(self, DomainStatus):
        self._DomainStatus = DomainStatus

    @property
    def BuyStatus(self):
        return self._BuyStatus

    @BuyStatus.setter
    def BuyStatus(self, BuyStatus):
        self._BuyStatus = BuyStatus

    @property
    def RegistrarType(self):
        return self._RegistrarType

    @RegistrarType.setter
    def RegistrarType(self, RegistrarType):
        self._RegistrarType = RegistrarType

    @property
    def NameServer(self):
        return self._NameServer

    @NameServer.setter
    def NameServer(self, NameServer):
        self._NameServer = NameServer

    @property
    def LockTransfer(self):
        return self._LockTransfer

    @LockTransfer.setter
    def LockTransfer(self, LockTransfer):
        self._LockTransfer = LockTransfer

    @property
    def LockEndTime(self):
        return self._LockEndTime

    @LockEndTime.setter
    def LockEndTime(self, LockEndTime):
        self._LockEndTime = LockEndTime

    @property
    def RegistrantType(self):
        return self._RegistrantType

    @RegistrantType.setter
    def RegistrantType(self, RegistrantType):
        self._RegistrantType = RegistrantType

    @property
    def OrganizationNameCN(self):
        return self._OrganizationNameCN

    @OrganizationNameCN.setter
    def OrganizationNameCN(self, OrganizationNameCN):
        self._OrganizationNameCN = OrganizationNameCN

    @property
    def OrganizationName(self):
        return self._OrganizationName

    @OrganizationName.setter
    def OrganizationName(self, OrganizationName):
        self._OrganizationName = OrganizationName

    @property
    def RegistrantNameCN(self):
        return self._RegistrantNameCN

    @RegistrantNameCN.setter
    def RegistrantNameCN(self, RegistrantNameCN):
        self._RegistrantNameCN = RegistrantNameCN

    @property
    def RegistrantName(self):
        return self._RegistrantName

    @RegistrantName.setter
    def RegistrantName(self, RegistrantName):
        self._RegistrantName = RegistrantName


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DomainName = params.get("DomainName")
        self._RealNameAuditStatus = params.get("RealNameAuditStatus")
        self._RealNameAuditUnpassReason = params.get("RealNameAuditUnpassReason")
        self._DomainNameAuditStatus = params.get("DomainNameAuditStatus")
        self._DomainNameAuditUnpassReason = params.get("DomainNameAuditUnpassReason")
        self._CreationDate = params.get("CreationDate")
        self._ExpirationDate = params.get("ExpirationDate")
        self._DomainStatus = params.get("DomainStatus")
        self._BuyStatus = params.get("BuyStatus")
        self._RegistrarType = params.get("RegistrarType")
        self._NameServer = params.get("NameServer")
        self._LockTransfer = params.get("LockTransfer")
        self._LockEndTime = params.get("LockEndTime")
        self._RegistrantType = params.get("RegistrantType")
        self._OrganizationNameCN = params.get("OrganizationNameCN")
        self._OrganizationName = params.get("OrganizationName")
        self._RegistrantNameCN = params.get("RegistrantNameCN")
        self._RegistrantName = params.get("RegistrantName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FailReservedDomainInfo(AbstractModel):
    """失败预约预释放域名信息

    """

    def __init__(self):
        r"""
        :param _Domain: 域名
注意：此字段可能返回 null，表示取不到有效值。
        :type Domain: str
        :param _FailReason: 预约失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailReason: str
        """
        self._Domain = None
        self._FailReason = None

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def FailReason(self):
        return self._FailReason

    @FailReason.setter
    def FailReason(self, FailReason):
        self._FailReason = FailReason


    def _deserialize(self, params):
        self._Domain = params.get("Domain")
        self._FailReason = params.get("FailReason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCustomDnsHostRequest(AbstractModel):
    """ModifyCustomDnsHost请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名实例ID
        :type DomainId: str
        :param _DnsName: DNS名称
        :type DnsName: str
        :param _IpSet: IP地址列表
        :type IpSet: list of str
        """
        self._DomainId = None
        self._DnsName = None
        self._IpSet = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DnsName(self):
        return self._DnsName

    @DnsName.setter
    def DnsName(self, DnsName):
        self._DnsName = DnsName

    @property
    def IpSet(self):
        return self._IpSet

    @IpSet.setter
    def IpSet(self, IpSet):
        self._IpSet = IpSet


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DnsName = params.get("DnsName")
        self._IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCustomDnsHostResponse(AbstractModel):
    """ModifyCustomDnsHost返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 异步任务ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class ModifyDomainDNSBatchRequest(AbstractModel):
    """ModifyDomainDNSBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 批量操作的域名。
        :type Domains: list of str
        :param _Dns: 域名DNS 数组。
        :type Dns: list of str
        """
        self._Domains = None
        self._Dns = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def Dns(self):
        return self._Dns

    @Dns.setter
    def Dns(self, Dns):
        self._Dns = Dns


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._Dns = params.get("Dns")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDomainDNSBatchResponse(AbstractModel):
    """ModifyDomainDNSBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID。
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class ModifyDomainOwnerBatchRequest(AbstractModel):
    """ModifyDomainOwnerBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 要过户的域名。
        :type Domains: list of str
        :param _NewOwnerUin: 转入账户的uin。
        :type NewOwnerUin: str
        :param _TransferDns: 是否同时转移对应的 DNS 解析域名，默认false
        :type TransferDns: bool
        :param _NewOwnerAppId: 转入账户的appid。
        :type NewOwnerAppId: str
        """
        self._Domains = None
        self._NewOwnerUin = None
        self._TransferDns = None
        self._NewOwnerAppId = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def NewOwnerUin(self):
        return self._NewOwnerUin

    @NewOwnerUin.setter
    def NewOwnerUin(self, NewOwnerUin):
        self._NewOwnerUin = NewOwnerUin

    @property
    def TransferDns(self):
        return self._TransferDns

    @TransferDns.setter
    def TransferDns(self, TransferDns):
        self._TransferDns = TransferDns

    @property
    def NewOwnerAppId(self):
        return self._NewOwnerAppId

    @NewOwnerAppId.setter
    def NewOwnerAppId(self, NewOwnerAppId):
        self._NewOwnerAppId = NewOwnerAppId


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._NewOwnerUin = params.get("NewOwnerUin")
        self._TransferDns = params.get("TransferDns")
        self._NewOwnerAppId = params.get("NewOwnerAppId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDomainOwnerBatchResponse(AbstractModel):
    """ModifyDomainOwnerBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志id
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class ModifyIntlCustomDnsHostRequest(AbstractModel):
    """ModifyIntlCustomDnsHost请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名ID
        :type DomainId: str
        :param _DnsName: DNS Host
        :type DnsName: str
        :param _IpSet: IP地址
        :type IpSet: list of str
        """
        self._DomainId = None
        self._DnsName = None
        self._IpSet = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def DnsName(self):
        return self._DnsName

    @DnsName.setter
    def DnsName(self, DnsName):
        self._DnsName = DnsName

    @property
    def IpSet(self):
        return self._IpSet

    @IpSet.setter
    def IpSet(self, IpSet):
        self._IpSet = IpSet


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._DnsName = params.get("DnsName")
        self._IpSet = params.get("IpSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyIntlCustomDnsHostResponse(AbstractModel):
    """ModifyIntlCustomDnsHost返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 任务ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class PhoneEmailData(AbstractModel):
    """手机号邮箱列表

    """

    def __init__(self):
        r"""
        :param _Code: 手机号或者邮箱
        :type Code: str
        :param _Type: 1：手机  2：邮箱
        :type Type: int
        :param _CreatedOn: 创建时间
        :type CreatedOn: str
        :param _CheckStatus: 1=控制台校验，2=第三方校验
        :type CheckStatus: int
        """
        self._Code = None
        self._Type = None
        self._CreatedOn = None
        self._CheckStatus = None

    @property
    def Code(self):
        return self._Code

    @Code.setter
    def Code(self, Code):
        self._Code = Code

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def CreatedOn(self):
        return self._CreatedOn

    @CreatedOn.setter
    def CreatedOn(self, CreatedOn):
        self._CreatedOn = CreatedOn

    @property
    def CheckStatus(self):
        return self._CheckStatus

    @CheckStatus.setter
    def CheckStatus(self, CheckStatus):
        self._CheckStatus = CheckStatus


    def _deserialize(self, params):
        self._Code = params.get("Code")
        self._Type = params.get("Type")
        self._CreatedOn = params.get("CreatedOn")
        self._CheckStatus = params.get("CheckStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PriceInfo(AbstractModel):
    """域名价格信息

    """

    def __init__(self):
        r"""
        :param _Tld: 域名后缀，例如.com
        :type Tld: str
        :param _Year: 购买年限，范围[1-10]
        :type Year: int
        :param _Price: 域名原价
        :type Price: int
        :param _RealPrice: 域名现价
        :type RealPrice: int
        :param _Operation: 商品的购买类型，新购，续费，赎回，转入，续费并转入
        :type Operation: str
        """
        self._Tld = None
        self._Year = None
        self._Price = None
        self._RealPrice = None
        self._Operation = None

    @property
    def Tld(self):
        return self._Tld

    @Tld.setter
    def Tld(self, Tld):
        self._Tld = Tld

    @property
    def Year(self):
        return self._Year

    @Year.setter
    def Year(self, Year):
        self._Year = Year

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, Price):
        self._Price = Price

    @property
    def RealPrice(self):
        return self._RealPrice

    @RealPrice.setter
    def RealPrice(self, RealPrice):
        self._RealPrice = RealPrice

    @property
    def Operation(self):
        return self._Operation

    @Operation.setter
    def Operation(self, Operation):
        self._Operation = Operation


    def _deserialize(self, params):
        self._Tld = params.get("Tld")
        self._Year = params.get("Year")
        self._Price = params.get("Price")
        self._RealPrice = params.get("RealPrice")
        self._Operation = params.get("Operation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewDomainBatchRequest(AbstractModel):
    """RenewDomainBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Period: 域名续费的年限。
        :type Period: int
        :param _Domains: 批量续费的域名。
        :type Domains: list of str
        :param _PayMode: 付费模式 0手动在线付费，1使用余额付费，2使用特惠包。
        :type PayMode: int
        :param _AutoRenewFlag: 自动续费开关。有三个可选值：
0 表示关闭，不自动续费
1 表示开启，将自动续费
2 表示不处理，保留域名原有状态（默认值）
        :type AutoRenewFlag: int
        :param _PackageResourceId: 特惠包ID
        :type PackageResourceId: str
        :param _ChannelFrom: 渠道来源，pc/miniprogram/h5等
        :type ChannelFrom: str
        :param _OrderFrom: 订单来源，common正常/dianshi_active点石活动等
        :type OrderFrom: str
        :param _ActivityId: 活动id
        :type ActivityId: str
        """
        self._Period = None
        self._Domains = None
        self._PayMode = None
        self._AutoRenewFlag = None
        self._PackageResourceId = None
        self._ChannelFrom = None
        self._OrderFrom = None
        self._ActivityId = None

    @property
    def Period(self):
        return self._Period

    @Period.setter
    def Period(self, Period):
        self._Period = Period

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def PayMode(self):
        return self._PayMode

    @PayMode.setter
    def PayMode(self, PayMode):
        self._PayMode = PayMode

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def PackageResourceId(self):
        return self._PackageResourceId

    @PackageResourceId.setter
    def PackageResourceId(self, PackageResourceId):
        self._PackageResourceId = PackageResourceId

    @property
    def ChannelFrom(self):
        return self._ChannelFrom

    @ChannelFrom.setter
    def ChannelFrom(self, ChannelFrom):
        self._ChannelFrom = ChannelFrom

    @property
    def OrderFrom(self):
        return self._OrderFrom

    @OrderFrom.setter
    def OrderFrom(self, OrderFrom):
        self._OrderFrom = OrderFrom

    @property
    def ActivityId(self):
        return self._ActivityId

    @ActivityId.setter
    def ActivityId(self, ActivityId):
        self._ActivityId = ActivityId


    def _deserialize(self, params):
        self._Period = params.get("Period")
        self._Domains = params.get("Domains")
        self._PayMode = params.get("PayMode")
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._PackageResourceId = params.get("PackageResourceId")
        self._ChannelFrom = params.get("ChannelFrom")
        self._OrderFrom = params.get("OrderFrom")
        self._ActivityId = params.get("ActivityId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewDomainBatchResponse(AbstractModel):
    """RenewDomainBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 操作日志ID。
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class ReservedDomainInfo(AbstractModel):
    """查询预释放预约列表域名详情

    """

    def __init__(self):
        r"""
        :param _Domain: 域名
        :type Domain: str
        :param _RegTime: 注册时间
        :type RegTime: str
        :param _ExpireTime: 到期时间
        :type ExpireTime: str
        :param _RenewEndTime: 续费时间结束
        :type RenewEndTime: str
        :param _RestoreEndTime: 赎回结束时间
        :type RestoreEndTime: str
        :param _ReservedEndTime: 域名预约结束时间
        :type ReservedEndTime: str
        """
        self._Domain = None
        self._RegTime = None
        self._ExpireTime = None
        self._RenewEndTime = None
        self._RestoreEndTime = None
        self._ReservedEndTime = None

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def RegTime(self):
        return self._RegTime

    @RegTime.setter
    def RegTime(self, RegTime):
        self._RegTime = RegTime

    @property
    def ExpireTime(self):
        return self._ExpireTime

    @ExpireTime.setter
    def ExpireTime(self, ExpireTime):
        self._ExpireTime = ExpireTime

    @property
    def RenewEndTime(self):
        return self._RenewEndTime

    @RenewEndTime.setter
    def RenewEndTime(self, RenewEndTime):
        self._RenewEndTime = RenewEndTime

    @property
    def RestoreEndTime(self):
        return self._RestoreEndTime

    @RestoreEndTime.setter
    def RestoreEndTime(self, RestoreEndTime):
        self._RestoreEndTime = RestoreEndTime

    @property
    def ReservedEndTime(self):
        return self._ReservedEndTime

    @ReservedEndTime.setter
    def ReservedEndTime(self, ReservedEndTime):
        self._ReservedEndTime = ReservedEndTime


    def _deserialize(self, params):
        self._Domain = params.get("Domain")
        self._RegTime = params.get("RegTime")
        self._ExpireTime = params.get("ExpireTime")
        self._RenewEndTime = params.get("RenewEndTime")
        self._RestoreEndTime = params.get("RestoreEndTime")
        self._ReservedEndTime = params.get("ReservedEndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReservedPreDomainInfo(AbstractModel):
    """预约预释放域名详情信息

    """

    def __init__(self):
        r"""
        :param _Domain: 域名
        :type Domain: str
        :param _ReservedStatus: 1. 预定成功 2. 预定失败（预定失败Reason字段将会被赋值）3. 域名交割中 4. 域名交割完成
        :type ReservedStatus: int
        :param _FailReason: 域名预定失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailReason: str
        :param _ChangeOwnerTime: 预计变更所有权时间（仅用于参考，实际时间会存在误差）
注意：此字段可能返回 null，表示取不到有效值。
        :type ChangeOwnerTime: str
        :param _RegTime: 注册时间
注意：此字段可能返回 null，表示取不到有效值。
        :type RegTime: str
        :param _ExpireTime: 到期时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireTime: str
        :param _ResourceId: 资源ID，用于删除资源信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceId: str
        """
        self._Domain = None
        self._ReservedStatus = None
        self._FailReason = None
        self._ChangeOwnerTime = None
        self._RegTime = None
        self._ExpireTime = None
        self._ResourceId = None

    @property
    def Domain(self):
        return self._Domain

    @Domain.setter
    def Domain(self, Domain):
        self._Domain = Domain

    @property
    def ReservedStatus(self):
        return self._ReservedStatus

    @ReservedStatus.setter
    def ReservedStatus(self, ReservedStatus):
        self._ReservedStatus = ReservedStatus

    @property
    def FailReason(self):
        return self._FailReason

    @FailReason.setter
    def FailReason(self, FailReason):
        self._FailReason = FailReason

    @property
    def ChangeOwnerTime(self):
        return self._ChangeOwnerTime

    @ChangeOwnerTime.setter
    def ChangeOwnerTime(self, ChangeOwnerTime):
        self._ChangeOwnerTime = ChangeOwnerTime

    @property
    def RegTime(self):
        return self._RegTime

    @RegTime.setter
    def RegTime(self, RegTime):
        self._RegTime = RegTime

    @property
    def ExpireTime(self):
        return self._ExpireTime

    @ExpireTime.setter
    def ExpireTime(self, ExpireTime):
        self._ExpireTime = ExpireTime

    @property
    def ResourceId(self):
        return self._ResourceId

    @ResourceId.setter
    def ResourceId(self, ResourceId):
        self._ResourceId = ResourceId


    def _deserialize(self, params):
        self._Domain = params.get("Domain")
        self._ReservedStatus = params.get("ReservedStatus")
        self._FailReason = params.get("FailReason")
        self._ChangeOwnerTime = params.get("ChangeOwnerTime")
        self._RegTime = params.get("RegTime")
        self._ExpireTime = params.get("ExpireTime")
        self._ResourceId = params.get("ResourceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReservedPreDomainsRequest(AbstractModel):
    """ReservedPreDomains请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainList: 预约预释放域名列表
        :type DomainList: list of str
        :param _TemplateId: 模板ID
        :type TemplateId: str
        """
        self._DomainList = None
        self._TemplateId = None

    @property
    def DomainList(self):
        return self._DomainList

    @DomainList.setter
    def DomainList(self, DomainList):
        self._DomainList = DomainList

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId


    def _deserialize(self, params):
        self._DomainList = params.get("DomainList")
        self._TemplateId = params.get("TemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ReservedPreDomainsResponse(AbstractModel):
    """ReservedPreDomains返回参数结构体

    """

    def __init__(self):
        r"""
        :param _SucDomainList: 预定成功域名列表
        :type SucDomainList: list of str
        :param _FailDomainList: 预定失败域名列表
        :type FailDomainList: list of FailReservedDomainInfo
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._SucDomainList = None
        self._FailDomainList = None
        self._RequestId = None

    @property
    def SucDomainList(self):
        return self._SucDomainList

    @SucDomainList.setter
    def SucDomainList(self, SucDomainList):
        self._SucDomainList = SucDomainList

    @property
    def FailDomainList(self):
        return self._FailDomainList

    @FailDomainList.setter
    def FailDomainList(self, FailDomainList):
        self._FailDomainList = FailDomainList

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._SucDomainList = params.get("SucDomainList")
        if params.get("FailDomainList") is not None:
            self._FailDomainList = []
            for item in params.get("FailDomainList"):
                obj = FailReservedDomainInfo()
                obj._deserialize(item)
                self._FailDomainList.append(obj)
        self._RequestId = params.get("RequestId")


class SendPhoneEmailCodeRequest(AbstractModel):
    """SendPhoneEmailCode请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Code: 手机或者邮箱号。
        :type Code: str
        :param _Type: 1：手机  2：邮箱。
        :type Type: int
        """
        self._Code = None
        self._Type = None

    @property
    def Code(self):
        return self._Code

    @Code.setter
    def Code(self, Code):
        self._Code = Code

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type


    def _deserialize(self, params):
        self._Code = params.get("Code")
        self._Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SendPhoneEmailCodeResponse(AbstractModel):
    """SendPhoneEmailCode返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class SetDomainAutoRenewRequest(AbstractModel):
    """SetDomainAutoRenew请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名ID 例如：domain-123abc
        :type DomainId: str
        :param _AutoRenew: AutoRenew 有三个可选值：
 0：不设置自动续费
1：设置自动续费
2：设置到期后不续费
        :type AutoRenew: int
        """
        self._DomainId = None
        self._AutoRenew = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId

    @property
    def AutoRenew(self):
        return self._AutoRenew

    @AutoRenew.setter
    def AutoRenew(self, AutoRenew):
        self._AutoRenew = AutoRenew


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        self._AutoRenew = params.get("AutoRenew")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetDomainAutoRenewResponse(AbstractModel):
    """SetDomainAutoRenew返回参数结构体

    """

    def __init__(self):
        r"""
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class SyncCustomDnsHostRequest(AbstractModel):
    """SyncCustomDnsHost请求参数结构体

    """

    def __init__(self):
        r"""
        :param _DomainId: 域名实例ID
        :type DomainId: str
        """
        self._DomainId = None

    @property
    def DomainId(self):
        return self._DomainId

    @DomainId.setter
    def DomainId(self, DomainId):
        self._DomainId = DomainId


    def _deserialize(self, params):
        self._DomainId = params.get("DomainId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SyncCustomDnsHostResponse(AbstractModel):
    """SyncCustomDnsHost返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 异步任务ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class TemplateInfo(AbstractModel):
    """Template数据

    """

    def __init__(self):
        r"""
        :param _TemplateId: 模板ID
        :type TemplateId: str
        :param _AuditStatus: 认证状态：未实名认证:NotUpload, 实名审核中:InAudit，已实名认证:Approved，实名审核失败:Reject
        :type AuditStatus: str
        :param _CreatedOn: 创建时间
        :type CreatedOn: str
        :param _UpdatedOn: 更新时间
        :type UpdatedOn: str
        :param _UserUin: 用户UIN
        :type UserUin: str
        :param _IsDefault: 是否是默认模板: 是:yes，否:no
        :type IsDefault: str
        :param _AuditReason: 认证失败原因
        :type AuditReason: str
        :param _CertificateInfo: 认证信息
        :type CertificateInfo: :class:`tencentcloud.domain.v20180808.models.CertificateInfo`
        :param _ContactInfo: 联系人信息
        :type ContactInfo: :class:`tencentcloud.domain.v20180808.models.ContactInfo`
        :param _IsValidTemplate: 模板是否符合规范， 1是 0 否
        :type IsValidTemplate: int
        :param _InvalidReason: 不符合规范原因
        :type InvalidReason: str
        :param _IsBlack: 是包含黑名单手机或邮箱
        :type IsBlack: bool
        """
        self._TemplateId = None
        self._AuditStatus = None
        self._CreatedOn = None
        self._UpdatedOn = None
        self._UserUin = None
        self._IsDefault = None
        self._AuditReason = None
        self._CertificateInfo = None
        self._ContactInfo = None
        self._IsValidTemplate = None
        self._InvalidReason = None
        self._IsBlack = None

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def AuditStatus(self):
        return self._AuditStatus

    @AuditStatus.setter
    def AuditStatus(self, AuditStatus):
        self._AuditStatus = AuditStatus

    @property
    def CreatedOn(self):
        return self._CreatedOn

    @CreatedOn.setter
    def CreatedOn(self, CreatedOn):
        self._CreatedOn = CreatedOn

    @property
    def UpdatedOn(self):
        return self._UpdatedOn

    @UpdatedOn.setter
    def UpdatedOn(self, UpdatedOn):
        self._UpdatedOn = UpdatedOn

    @property
    def UserUin(self):
        return self._UserUin

    @UserUin.setter
    def UserUin(self, UserUin):
        self._UserUin = UserUin

    @property
    def IsDefault(self):
        return self._IsDefault

    @IsDefault.setter
    def IsDefault(self, IsDefault):
        self._IsDefault = IsDefault

    @property
    def AuditReason(self):
        return self._AuditReason

    @AuditReason.setter
    def AuditReason(self, AuditReason):
        self._AuditReason = AuditReason

    @property
    def CertificateInfo(self):
        return self._CertificateInfo

    @CertificateInfo.setter
    def CertificateInfo(self, CertificateInfo):
        self._CertificateInfo = CertificateInfo

    @property
    def ContactInfo(self):
        return self._ContactInfo

    @ContactInfo.setter
    def ContactInfo(self, ContactInfo):
        self._ContactInfo = ContactInfo

    @property
    def IsValidTemplate(self):
        return self._IsValidTemplate

    @IsValidTemplate.setter
    def IsValidTemplate(self, IsValidTemplate):
        self._IsValidTemplate = IsValidTemplate

    @property
    def InvalidReason(self):
        return self._InvalidReason

    @InvalidReason.setter
    def InvalidReason(self, InvalidReason):
        self._InvalidReason = InvalidReason

    @property
    def IsBlack(self):
        return self._IsBlack

    @IsBlack.setter
    def IsBlack(self, IsBlack):
        self._IsBlack = IsBlack


    def _deserialize(self, params):
        self._TemplateId = params.get("TemplateId")
        self._AuditStatus = params.get("AuditStatus")
        self._CreatedOn = params.get("CreatedOn")
        self._UpdatedOn = params.get("UpdatedOn")
        self._UserUin = params.get("UserUin")
        self._IsDefault = params.get("IsDefault")
        self._AuditReason = params.get("AuditReason")
        if params.get("CertificateInfo") is not None:
            self._CertificateInfo = CertificateInfo()
            self._CertificateInfo._deserialize(params.get("CertificateInfo"))
        if params.get("ContactInfo") is not None:
            self._ContactInfo = ContactInfo()
            self._ContactInfo._deserialize(params.get("ContactInfo"))
        self._IsValidTemplate = params.get("IsValidTemplate")
        self._InvalidReason = params.get("InvalidReason")
        self._IsBlack = params.get("IsBlack")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TransferInDomainBatchRequest(AbstractModel):
    """TransferInDomainBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 转入的域名名称数组。
        :type Domains: list of str
        :param _PassWords: 域名转移码数组。
        :type PassWords: list of str
        :param _TemplateId: 模板ID。
        :type TemplateId: str
        :param _PayMode: 付费模式 0手动在线付费，1使用余额付费。
        :type PayMode: int
        :param _AutoRenewFlag: 自动续费开关。有两个可选值：
0 表示关闭，不自动续费（默认值）
1 表示开启，将自动续费
        :type AutoRenewFlag: int
        :param _LockTransfer: true： 开启60天内禁止转移注册商锁定
false：关闭60天内禁止转移注册商锁定
默认 true
        :type LockTransfer: bool
        :param _UpdateProhibition: 是否开启更新锁：0=默认不开启，1=开启
        :type UpdateProhibition: int
        :param _TransferProhibition: 是否开启转移锁：0=默认不开启，1=开启
        :type TransferProhibition: int
        :param _ChannelFrom: 渠道来源，pc/miniprogram/h5等
        :type ChannelFrom: str
        :param _OrderFrom: 订单来源，common正常/dianshi_active点石活动等
        :type OrderFrom: str
        :param _ActivityId: 活动id
        :type ActivityId: str
        """
        self._Domains = None
        self._PassWords = None
        self._TemplateId = None
        self._PayMode = None
        self._AutoRenewFlag = None
        self._LockTransfer = None
        self._UpdateProhibition = None
        self._TransferProhibition = None
        self._ChannelFrom = None
        self._OrderFrom = None
        self._ActivityId = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def PassWords(self):
        return self._PassWords

    @PassWords.setter
    def PassWords(self, PassWords):
        self._PassWords = PassWords

    @property
    def TemplateId(self):
        return self._TemplateId

    @TemplateId.setter
    def TemplateId(self, TemplateId):
        self._TemplateId = TemplateId

    @property
    def PayMode(self):
        return self._PayMode

    @PayMode.setter
    def PayMode(self, PayMode):
        self._PayMode = PayMode

    @property
    def AutoRenewFlag(self):
        return self._AutoRenewFlag

    @AutoRenewFlag.setter
    def AutoRenewFlag(self, AutoRenewFlag):
        self._AutoRenewFlag = AutoRenewFlag

    @property
    def LockTransfer(self):
        return self._LockTransfer

    @LockTransfer.setter
    def LockTransfer(self, LockTransfer):
        self._LockTransfer = LockTransfer

    @property
    def UpdateProhibition(self):
        return self._UpdateProhibition

    @UpdateProhibition.setter
    def UpdateProhibition(self, UpdateProhibition):
        self._UpdateProhibition = UpdateProhibition

    @property
    def TransferProhibition(self):
        return self._TransferProhibition

    @TransferProhibition.setter
    def TransferProhibition(self, TransferProhibition):
        self._TransferProhibition = TransferProhibition

    @property
    def ChannelFrom(self):
        return self._ChannelFrom

    @ChannelFrom.setter
    def ChannelFrom(self, ChannelFrom):
        self._ChannelFrom = ChannelFrom

    @property
    def OrderFrom(self):
        return self._OrderFrom

    @OrderFrom.setter
    def OrderFrom(self, OrderFrom):
        self._OrderFrom = OrderFrom

    @property
    def ActivityId(self):
        return self._ActivityId

    @ActivityId.setter
    def ActivityId(self, ActivityId):
        self._ActivityId = ActivityId


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._PassWords = params.get("PassWords")
        self._TemplateId = params.get("TemplateId")
        self._PayMode = params.get("PayMode")
        self._AutoRenewFlag = params.get("AutoRenewFlag")
        self._LockTransfer = params.get("LockTransfer")
        self._UpdateProhibition = params.get("UpdateProhibition")
        self._TransferProhibition = params.get("TransferProhibition")
        self._ChannelFrom = params.get("ChannelFrom")
        self._OrderFrom = params.get("OrderFrom")
        self._ActivityId = params.get("ActivityId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TransferInDomainBatchResponse(AbstractModel):
    """TransferInDomainBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class TransferProhibitionBatchRequest(AbstractModel):
    """TransferProhibitionBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 批量操作的域名。
        :type Domains: list of str
        :param _Status: 是否开启禁止域名转移。
True: 开启禁止域名转移状态。
False：关闭禁止域名转移状态。
        :type Status: bool
        """
        self._Domains = None
        self._Status = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TransferProhibitionBatchResponse(AbstractModel):
    """TransferProhibitionBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class UpdateProhibitionBatchRequest(AbstractModel):
    """UpdateProhibitionBatch请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Domains: 批量操作的域名。
        :type Domains: list of str
        :param _Status: 是否开启禁止域名更新。
True:开启禁止域名更新状态。
False：关闭禁止域名更新状态。
        :type Status: bool
        """
        self._Domains = None
        self._Status = None

    @property
    def Domains(self):
        return self._Domains

    @Domains.setter
    def Domains(self, Domains):
        self._Domains = Domains

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status


    def _deserialize(self, params):
        self._Domains = params.get("Domains")
        self._Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateProhibitionBatchResponse(AbstractModel):
    """UpdateProhibitionBatch返回参数结构体

    """

    def __init__(self):
        r"""
        :param _LogId: 日志ID
        :type LogId: int
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._LogId = None
        self._RequestId = None

    @property
    def LogId(self):
        return self._LogId

    @LogId.setter
    def LogId(self, LogId):
        self._LogId = LogId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._LogId = params.get("LogId")
        self._RequestId = params.get("RequestId")


class UploadImageRequest(AbstractModel):
    """UploadImage请求参数结构体

    """

    def __init__(self):
        r"""
        :param _ImageFile: 资质照片，照片的base64编码。
        :type ImageFile: str
        """
        self._ImageFile = None

    @property
    def ImageFile(self):
        return self._ImageFile

    @ImageFile.setter
    def ImageFile(self, ImageFile):
        self._ImageFile = ImageFile


    def _deserialize(self, params):
        self._ImageFile = params.get("ImageFile")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UploadImageResponse(AbstractModel):
    """UploadImage返回参数结构体

    """

    def __init__(self):
        r"""
        :param _AccessUrl: 资质照片地址。
        :type AccessUrl: str
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._AccessUrl = None
        self._RequestId = None

    @property
    def AccessUrl(self):
        return self._AccessUrl

    @AccessUrl.setter
    def AccessUrl(self, AccessUrl):
        self._AccessUrl = AccessUrl

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._AccessUrl = params.get("AccessUrl")
        self._RequestId = params.get("RequestId")