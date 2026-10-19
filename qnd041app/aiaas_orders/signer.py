from firma_xades.firma import XAdESBESSigner

def firmar_xml(xml_str, path_certificado, password_certificado):
    signer = XAdESBESSigner()
    with open(path_certificado, 'rb') as cert_file:
        certificado = cert_file.read()
    signed_xml = signer.sign(xml_str, certificado, password_certificado)
    return signed_xml
