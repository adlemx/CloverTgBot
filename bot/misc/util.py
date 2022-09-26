import base64
import io

import qrcode


def generate_qr(code: int) -> io.BytesIO:
    buffer = io.BytesIO()
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12
    )
    QRcode.add_data(code)
    QRcode.make()
    QRimg = QRcode.make_image()
    QRimg.save(buffer, format="PNG")
    encoded = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")
    return buffer