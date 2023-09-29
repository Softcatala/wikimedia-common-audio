import unittest
from extract import TextExtract

class TestExtract(unittest.TestCase):

    case_1 = """
-------------------------------
title: Ca-Ogg Vorbis-article.ogg
license: PD-self
description: Gravació de l'article Ogg Vorbis de la Viquipèdia en català.
full text: == {{int:filedesc}} ==
{{Information
 |description = {{ca|1=Gravació de l'article Ogg Vorbis de la Viquipèdia en català.}}
}}

== {{int:license-header}} ==
{{PD-self}}

"""

    def test_textextract_license_case_1(self):
        title, description, license = TextExtract(self.case_1).GetDescription()
        self.assertEqual("PD-self", license)

    case_2 = """
title: LS FLORS DE MAIG.ogg
license: cc-by-sa-3.0
description: peça coral del Josep A. Clavé
full text: =={{int:filedesc}}==
{{Information
|description={{ca|1=peça coral del Josep A. Clavé}}
|date=2011-12-02
|source={{own}}
|author=[[User:Albasagitario|Albasagitario]]
|permission=
|other_versions=
|other_fields=
}}

=={{int:license-header}}==

{{self|cc-by-sa-3.0}}
    
"""

    def test_textextract_license_case_2(self):
        title, description, license = TextExtract(self.case_2).GetDescription()
        self.assertEqual("cc-by-sa-3.0", license)





    case_3 = """
title: LS FLORS DE MAIG.ogg
license: cc-by-sa-3.0
description: peça coral del Josep A. Clavé
full text: =={{int:filedesc}}==
{{Information
|description={{ca|1=peça coral del Josep A. Clavé}}
|date=2011-12-02
|source={{own}}
|author=[[User:Albasagitario|Albasagitario]]
|permission=
|other_versions=
|other_fields=
}}

=={{int:license-header}}==

{{self|cc-by-sa-4.0}} {{ANOTHER}}
    
"""

    def test_textextract_license_case_3(self):
        title, description, license = TextExtract(self.case_3).GetDescription()
        self.assertEqual("cc-by-sa-4.0", license)

    case_4 = """
title: Andreu Banyuls - voice.ogg
license: Ràdio Godella-imatge}}{{CC-BY-SA 4.0
description: Autopresentació d'Andreu Banyuls
full text: =={{int:filedesc}}==
{{Information
|description={{ca|1=Autopresentació d'Andreu Banyuls}}
|date=2017-04-06
|source={{own}}
|author=[[User:TaronjaSatsuma|Francesc Fort]]
|permission=
|other versions=
}}

=={{int:license-header}}==
{{Ràdio Godella}}{{CC-BY-SA 4.0}}
    
"""

    def test_textextract_license_case_4(self):
        title, description, license = TextExtract(self.case_4).GetDescription()
        self.assertEqual("CC-BY-SA 4.0", license)


    
