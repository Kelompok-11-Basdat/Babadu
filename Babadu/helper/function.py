
def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



def title_to_slug(text):
    return text.lower().replace(' ', '-')

def slug_to_title(slug):
    return slug.replace('-', ' ').title()

def format_rupiah(amount):
    rupiah = "Rp {:,}".format(amount).replace(',', '.')
    return rupiah
