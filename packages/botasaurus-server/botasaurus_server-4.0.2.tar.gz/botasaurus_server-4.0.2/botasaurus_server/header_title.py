from botasaurus.ip_utils import find_ip_details

def header_title():
    ip_details = find_ip_details()
    return  "ओमकार" if ip_details and ip_details.get('country') == 'IN' else "Omkar" 
