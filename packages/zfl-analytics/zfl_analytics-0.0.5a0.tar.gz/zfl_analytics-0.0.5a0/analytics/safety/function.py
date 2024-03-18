from django.core import signing  # type: ignore
from django.core.signing import Signer  # type:ignore


def encryption(target):
    """
    暗号化
    使用場所:models.py(カスタムユーザーのSaveメソッド)
    """
    signer = Signer()  # keyはデフォルトの「SECRET_KEY」を使用
    value = signer.sign(target)
    value_list = [value.split(":")]
    dict_sign = dict(value_list)
    signed_obj = signing.dumps(dict_sign)  # django==2.2.5
    # signed_obj = signer.sign_object(dict_sign)  # django==3.2.15
    return signed_obj


def decryption(target):
    """
    復号化
    使用場所:models.py(カスタムユーザーのSaveメソッド)
    """
    signer = Signer()  # keyはデフォルトの「SECRET_KEY」を使用
    # DB内で辞書を暗号化した要素を復号
    original = signing.loads(target)  # django==2.2.5
    # original = signer.unsign_object(target)  # django==3.2.15
    # 辞書内のキーとバリューを取り出す
    value_list = [k + ":" + v for k, v in original.items()]
    # リスト内には１つしか要素がないので０番目の要素を取り出す
    value = value_list[0]
    # 最後にテキストをsignした暗号物を復号する
    plain_text = signer.unsign(value)
    return plain_text
