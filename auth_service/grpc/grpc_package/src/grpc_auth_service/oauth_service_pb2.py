# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oauth_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13oauth_service.proto"^\n\x1aGetProviderLoginURLRequest\x12\x14\n\x0c\x63\x61llback_url\x18\x01 \x01(\t\x12\x19\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0f\n\r_access_token"?\n\x1bGetProviderLoginURLResponse\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x13\n\x0bstate_token\x18\x02 \x01(\t"6\n\x11OAuthLoginRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x13\n\x0bstate_token\x18\x02 \x01(\t"i\n\x12OAuthLoginResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x15\n\rrefresh_token\x18\x02 \x01(\t\x12\x12\n\nexpires_in\x18\x03 \x01(\r\x12\x12\n\ntoken_type\x18\x04 \x01(\t"U\n\x1a\x41ttachAccountToUserRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x13\n\x0bstate_token\x18\x03 \x01(\t"\x1d\n\x1b\x41ttachAccountToUserResponse"4\n\x1c\x44\x65tachAccountFromUserRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t"\x1f\n\x1d\x44\x65tachAccountFromUserResponse2\xbb\x02\n\x0bGoogleOAuth\x12P\n\x13GetProviderLoginURL\x12\x1b.GetProviderLoginURLRequest\x1a\x1c.GetProviderLoginURLResponse\x12\x30\n\x05Login\x12\x12.OAuthLoginRequest\x1a\x13.OAuthLoginResponse\x12P\n\x13\x41ttachAccountToUser\x12\x1b.AttachAccountToUserRequest\x1a\x1c.AttachAccountToUserResponse\x12V\n\x15\x44\x65tachAccountFromUser\x12\x1d.DetachAccountFromUserRequest\x1a\x1e.DetachAccountFromUserResponse2\xbb\x02\n\x0bYandexOAuth\x12P\n\x13GetProviderLoginURL\x12\x1b.GetProviderLoginURLRequest\x1a\x1c.GetProviderLoginURLResponse\x12\x30\n\x05Login\x12\x12.OAuthLoginRequest\x1a\x13.OAuthLoginResponse\x12P\n\x13\x41ttachAccountToUser\x12\x1b.AttachAccountToUserRequest\x1a\x1c.AttachAccountToUserResponse\x12V\n\x15\x44\x65tachAccountFromUser\x12\x1d.DetachAccountFromUserRequest\x1a\x1e.DetachAccountFromUserResponseb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "oauth_service_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS is False:

    DESCRIPTOR._options = None
    _GETPROVIDERLOGINURLREQUEST._serialized_start = 23
    _GETPROVIDERLOGINURLREQUEST._serialized_end = 117
    _GETPROVIDERLOGINURLRESPONSE._serialized_start = 119
    _GETPROVIDERLOGINURLRESPONSE._serialized_end = 182
    _OAUTHLOGINREQUEST._serialized_start = 184
    _OAUTHLOGINREQUEST._serialized_end = 238
    _OAUTHLOGINRESPONSE._serialized_start = 240
    _OAUTHLOGINRESPONSE._serialized_end = 345
    _ATTACHACCOUNTTOUSERREQUEST._serialized_start = 347
    _ATTACHACCOUNTTOUSERREQUEST._serialized_end = 432
    _ATTACHACCOUNTTOUSERRESPONSE._serialized_start = 434
    _ATTACHACCOUNTTOUSERRESPONSE._serialized_end = 463
    _DETACHACCOUNTFROMUSERREQUEST._serialized_start = 465
    _DETACHACCOUNTFROMUSERREQUEST._serialized_end = 517
    _DETACHACCOUNTFROMUSERRESPONSE._serialized_start = 519
    _DETACHACCOUNTFROMUSERRESPONSE._serialized_end = 550
    _GOOGLEOAUTH._serialized_start = 553
    _GOOGLEOAUTH._serialized_end = 868
    _YANDEXOAUTH._serialized_start = 871
    _YANDEXOAUTH._serialized_end = 1186
# @@protoc_insertion_point(module_scope)
