from lxml import etree

def generar_xml_factura(invoice):
    factura = etree.Element('factura', id="comprobante", version="1.0.0")

    infoTributaria = etree.SubElement(factura, 'infoTributaria')
    etree.SubElement(infoTributaria, 'razonSocial').text = "Mi Empresa"
    etree.SubElement(infoTributaria, 'ruc').text = "1234567890001"
    # Agrega más campos según el esquema del SRI

    infoFactura = etree.SubElement(factura, 'infoFactura')
    etree.SubElement(infoFactura, 'fechaEmision').text = invoice.date_issued.strftime('%d/%m/%Y')
    etree.SubElement(infoFactura, 'totalSinImpuestos').text = str(invoice.subtotal)
    etree.SubElement(infoFactura, 'importeTotal').text = str(invoice.total)
    
    return etree.tostring(factura, pretty_print=True, xml_declaration=True, encoding='UTF-8')
