# CODE STYLE

Chat ini akan membahas dan membantu penulisan kode untuk pembuatan modul odoo.

## A. Konteks Umum Yang Digunakan

1. Odoo 14
2. Mesin untuk developmemt menggunakan linux
3. Jangan menambahkan object sebagai contoh
4. Gunakan lisensi AGPL
5. Gunakan kutip dua
6. Gunakan 4 spasi untuk satu tab
7. Selalu gunakan list ketika inherit
8. Setiap object selalu dibuatkan file .py terpisah
9. Tambahkan komen berikut di awal tiap file .xml

```xml
<!-- Copyright ${tahun saat ini} OpenSynergy Indonesia
     Copyright ${tahun saat ini} PT. Simetri Sinergi Indonesia
     License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). -->
```

10. Tambahkan komen berikut di awal tiap file .py

```python
# Copyright ${tahun saat ini} OpenSynergy Indonesia
# Copyright ${tahun saat ini} PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
```

11. Jangan tambahkan field untuk tiap modul yang saya minta buat
12. Selalu gunakan named paramater pada pembuatam field

## B. Ketentuan Untuk Struktur Direktori

1. **init**.py hanya ada di root apabila ada wizard atau model yang ditambahkan
2. Buatkan direktori "security/ir_model_access" apabila ada object yang diinherit dari
   mixin.transaction
3. Buatkan direktori "security/res_groups" apabila ada object yang diinherit dari
   mixin.transaction
4. Buatkan direktori "security/ir_rule" apabila ada object yang diinherit dari
   mixin.transaction
5. Buatkan direktori "ir_sequence" apabila ada object yang diinherit dari
   mixin.transaction
6. Buatkan direktori "sequence_template" apabila ada object yang diinherit dari
   mixin.transaction
7. Buatkan direktori "policy_template" apabila ada object yang diinherit dari
   mixin.transaction
8. Buatkan direktori "approval_template" apabila ada object yang diinherit dari
   mixin.transaction
9. Buatkan direktori "security/ir_module_category" apabila ada object yang diinherit
   dari mixin.transaction

## C. Ketentuan untuk **manifest**.py

1. Author selalu OpenSynergy Indonesia, dan PT. Simetri Sinergi Indonesia
2. Apabila ada object yang diinherit dari mixin.master_data maka tambahkan dependensi
   module ke ssi_master_data_mixin. Pastikan ada object yang diinherit dari
   mixin.master_data sebelum dependensi ke ssi_master_data_mixin ditambahkan
3. Website: "https://simetri-sinergi.id"
4. Tidak perlu category
5. Tidak perlu summary
6. Kecuali disebutkan application selalu False

## D. Ketentuan untuk mixin.master_data

Lihat ketentuan di bawah apabila ada object yang diinherit dari mixin.master_data

1. Untuk masing-masing object baru yang diinherit dari mixin.master_data maka buatkan
   res.group dengan aturan:
   1. XML ID group adalah "\${nama*object*}configurator
   2. Nama group adalah "\${Nama Object}"
   3. parent_id dengarkan PARENT_GROUP_CONFIGURATOR yang akan saya berikan
2. Data group yang dibuat berdasarkan pada item nomor D.1 diletakan pada file
   /security/res_group.xml
3. Apabila ada lebih dari 1 object yang diinherit dari mixin.master_data maka data group
   dijadikan satu di /security/res_group.xml yang telah dibuat pada item D.2
4. Data untuk res.group jangan diberikan noupdate
5. Untuk masing-masing object baru yang diinherit dari mixin.master_data maka buatkan
   dua ir.model.access dengan aturan:
   1. ir.model.access pertama:
      1. XML ID: "\${nama_object}\_access_all"
      2. name: "\${Nama Object} - all"
      3. Berikan hanya akses read
      4. Berikan tanpa group
   2. ir.model.access kedua:
      1. XML ID: "\${nama_object}\_access_configurator"
      2. name: "\${Nama Object} - configurator"
      3. Berikan semua
      4. Berikan untuk group yang dibuat pada item D.1
6. Semua data ir.model.access dari item D.5 diletakan pada file
   /security/ir_model_access.xml
7. Jangan buat ir.rule untuk object yang diinherit dari mixin.master_data
8. Buatkan satu file xml untuk view object dengan format nama file
   "\${nama_object}\_views.xml"
9. Letakan file di direktori "/views"
10. Buat list, search, dan form view
11. Tambahkan windows action
12. Tambahkan menu.

### D.1. Ketentuan View, Window Action dan Master Data

1. Untuk masing-masing object baru yang diinherit dari mixin.master_data maka buatkan
   satu file pada direktori views.
2. Format nama file "\${nama_object}.xml"
3. Buatkan satu search view dengan format:

```xml
<record id="${name_object}_view_search" model="ir.ui.view">
        <field name="name">${name_object} - search</field>
        <field name="model">${name_object}</field>
    <field
    name="inherit_id"
    ref="ssi_master_data_mixin.mixin_master_data_view_search"
  />
    <field name="mode">primary</field>
    <field name="arch" type="xml">
        <data>
        </data>
    </field>
</record>
```

4. Buatkan satu tree view dengan format:

```xml
<record id="${name_object}_view_tree" model="ir.ui.view">
        <field name="name">${name_object} - tree</field>
        <field name="model">${name_object}</field>
    <field name="inherit_id" ref="ssi_master_data_mixin.mixin_master_data_view_tree" />
    <field name="mode">primary</field>
    <field name="arch" type="xml">
        <data>
            <xpath expr="//field[@name='name']" position="after">
            </xpath>
        </data>
    </field>
</record>
```

5. Buatkan satu form view dengan format:

```xml
<record id="${name_object}_view_form" model="ir.ui.view">
    <field name="name">${name_object} - form</field>
    <field name="model">${name_object}</field>
    <field name="mode">primary</field>
    <field name="inherit_id" ref="ssi_master_data_mixin.mixin_master_data_view_form" />
    <field name="arch" type="xml">
        <data>
            <xpath expr="//field[@name='active']" position="after">
            </xpath>
        </data>
    </field>
</record>
```

6. Buatkan satu ir.actions.act_window dengan format:

```xml
<record id="${name_object}_action" model="ir.actions.act_window">
    <field name="name">${Nama Object dalam bentuk plural}</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">${name_object}</field>
    <field name="view_mode">tree,form</field>
</record>
```

7. Buatkan satu menuitem dengan format:

```xml
<menuitem
  id="${name_object}_menu"
  name="Classes"
  action="${XML ID dari item 6}"
  groups="${group configuratornya}"
  parent="${berikan plaholder saja}"
/>
```

## E. Ketentuan untuk mixin.transaction

Lihat ketentuan di bawah apabila ada object yang diinherit dari mixin.transaction

### E.1 Ketentuan ir.module.category

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   dua ir.module.category dengan aturan:
   1. ir.module.category pertama:
      1. XML ID: "\${nama_object}\_workflow
      2. name: "\${Nama Object}"
      3. parent_id dengarkan PARENT_MODULE_WORKFLOW yang akan saya berikan
   2. ir.module.category kedua:
      1. XML ID: "\${nama_object}\_data_ownership
      2. name: "\${Nama Object}"
      3. parent_id dengarkan PARENT_MODULE_DATA_OWNERSHIP yang akan saya berikan
2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.9
4. Nama file untuk ir.module.category adalah \${nama_object}\_module_category.xml

### E.2 Ketentuan res.groups

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   res.groups dengan aturan:
   1. res.groups pertama:
      1. XML ID: "\${nama_object}\_viewer_group
      2. name: "Viewer"
      3. category_id diambil dari ir.module.category dari E.1.1.1
   2. res.groups kedua:
      1. XML ID: "\${nama_object}\_user_group
      2. name: "User"
      3. category_id diambil dari ir.module.category dari E.1.1.1
      4. parent_id diambil dari E.2.1.1
   3. res.groups ketiga:
      1. XML ID: "\${nama_object}\_validator_group
      2. name: "Validator"
      3. category_id diambil dari ir.module.category dari E.1.1.1
      4. parent_id diambil dari E.2.1.2
   4. res.groups keempat:
      1. XML ID: "\${nama_object}\_company_group
      2. name: "Company"
      3. category_id diambil dari ir.module.category dari E.1.1.2
   5. res.groups kelima:
      1. XML ID: "\${nama_object}\_child_company_group
      2. name: "Company and All Child Companies"
      3. category_id diambil dari ir.module.category dari E.1.1.2
      4. parent_id diambil dari E.2.1.4
   6. res.groups keenam:
      1. XML ID: "\${nama_object}\_all
      2. name: "All"
      3. category_id diambil dari ir.module.category dari E.1.1.2
      4. parent_id diambil dari E.2.1.4 5
2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.3
4. Nama file untuk res.groups adalah \${nama_object}.xml

### E.3 Ketentuan ir.model.access

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   ir.model.access dengan aturan:
   1. ir.model.access pertama:
      1. XML ID: "\${nama_object}\_all_access"
      2. name: "\${nama_object} - all"
      3. Berikan hanya read access
      4. Berikan ke semua user
   2. ir.model.access kedua:
      1. XML ID: "\${nama_object}\_user_access"
      2. name: "\${nama_object} - user"
      3. Berikan semua akses
      4. Berikan ke group dari E.2.1.2
2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.2
4. Nama file untuk ir.model.access adalah \${nama_object}.xml

### E.4 Ketentuan ir.rule

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   ir.rule dengan aturan:
   1. ir.rule pertama:
      1. XML ID: "\${nama_object}\_internal_user_rule"
      2. name: "\${nama_object} - Internal User"
      3. Berikan ke group "Internal User"
      4. Berikan semua akses
      5. Gunakan domain: [('user_id','=',user.id)]
   2. ir.rule kedua:
      1. XML ID: "\${nama_object}\_company_rule"
      2. name: "\${nama_object} - Responsible to company data"
      3. Berikan ke group dari E.2.1.4
      4. Berikan semua akses
      5. Gunakan domain: [('company_id','=',user.company_id.id)]
   3. ir.rule ketiga:
      1. XML ID: "\${nama_object}\_child_company_rule"
      2. name: "\${nama_object} - Responsible to company and all child companies data"
      3. Berikan ke group dari E.2.1.5
      4. Berikan semua akses
      5. Gunakan domain: [('company_id','in',user.company_ids.ids)]
   4. ir.rule keempay:
      1. XML ID: "\${nama_object}\_all_rule"
      2. name: "\${nama_object} - Responsible to all data"
      3. Berikan ke group dari E.2.1.6
      4. Berikan semua akses
      5. Gunakan domain: [(1,'=',1)]
2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.4
4. Nama file untuk ir.rule adalah \${nama_object}.xml

### E.5 Ketentuan ir.sequence

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   ir.sequence dengan format:

```xml
<record id="sequence_${nama_object}" model="ir.sequence">
    <field name="name">${Nama Object}$</field>
    <field name="code">${nama_object}</field>
    <field name="padding">6</field>
    <field
    name="prefix"
  >${Prefix sequence. Silahkan konbinasikan dari nama object}/%(range_year)s/</field>
    <field eval="1" name="number_next" />
    <field eval="1" name="number_increment" />
    <field name="use_date_range" eval="1" />
</record>
```

2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.5
4. Nama file adalah \${nama_object}.xml

### E.6 Ketentuan sequence_template

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   data sequence_template dengan format:

```xml
<record id="sequence_template_${nama_object}" model="sequence.template">
    <field name="name">Standard</field>
    <field name="model_id" ref="model_${nama_object}" />
    <field name="sequence" eval="100" />
    <field name="initial_string">/</field>
    <field
            name="sequence_field_id"
            search="[('model_id.model','=','${nama_object}'),('name','=','name')]"
        />
    <field
            name="date_field_id"
            search="[('model_id.model','=','${nama_object}'),('name','=','date')]"
        />
    <field name="computation_method">use_python</field>
    <field name="python_code">result=True</field>
    <field name="sequence_id" ref="${ir.sequence dari E.5.1}" />
    <field name="sequence_selection_method">use_sequence</field>
    <field name="add_custom_prefix" eval="0" />
    <field name="add_custom_suffix" eval="0" />
</record>
</record>
```

2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.6
4. Nama file adalah \${nama_object}.xml

### E.7 Ketentuan approval_template

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   data approval_template dengan format:

```xml
<record id="approval_template_${nama_object}" model="approval.template">
    <field name="name">Standard</field>
    <field name="model_id" ref="model_${nama_object}" />
    <field name="sequence" eval="100" />
    <field name="computation_method">use_python</field>
    <field name="python_code">result = True</field>
    <field name="validate_sequence" eval="1" />
</record>

<record id="approval_template_detail_${nama_object}" model="approval.template_detail">
    <field name="template_id" ref="approval_template_${nama_object}" />
    <field name="approver_selection_method">use_group</field>
    <field
            name="approver_group_ids"
            eval="[(6,0,[ref('${nama_object}_validator_group')])]"
        />
</record>
```

2. Buat 1 file per object yang diinherit dari mixin.transaction
3. File diletakan pada direktori yang dibuat pada item B.8
4. Nama file adalah \${nama_object}.xml

### E.9 Ketentuan Views, Windows Action, dan Menu

1. Untuk masing-masing object baru yang diinherit dari mixin.transaction maka buatkan
   satu file pada direktori views.
2. Format nama file "\${nama_object}\_views.xml"
3. Buatkan satu search view dengan format:

```xml
<record id="${name_object}_view_search" model="ir.ui.view">
        <field name="name">${name_object} - search</field>
        <field name="model">${name_object}</field>
    <field
    name="inherit_id"
    ref="ssi_transaction_mixin.mixin_transaction_view_search"
  />
    <field name="mode">primary</field>
    <field name="arch" type="xml">
        <data>
        </data>
    </field>
</record>
```

4. Buatkan satu tree view dengan format:

```xml
<record id="${name_object}_view_tree" model="ir.ui.view">
        <field name="name">${name_object} - tree</field>
        <field name="model">${name_object}</field>
    <field name="inherit_id" ref="ssi_transaction_mixin.mixin_transaction_view_tree" />
    <field name="mode">primary</field>
    <field name="arch" type="xml">
        <data>
            <xpath expr="//field[@name='company_id']" position="after">
            </xpath>
        </data>
    </field>
</record>
```

5. Buatkan satu form view dengan format:

```xml
<record id="${name_object}_view_form" model="ir.ui.view">
    <field name="name">${name_object} - form</field>
    <field name="model">${name_object}</field>
    <field name="mode">primary</field>
    <field name="inherit_id" ref="ssi_transaction_mixin.mixin_transaction_view_form" />
    <field name="arch" type="xml">
        <data>
            <xpath expr="//field[@name='user_id']" position="after">
            </xpath>
            <xpath expr="//group[@name='header_right']" position="inside">
            </xpath>
            <xpath expr="//page[1]" position="before">
            </xpath>
        </data>
    </field>
</record>
```

6. Buatkan satu ir.actions.act_window dengan format:

```xml
<record id="${name_object}_action" model="ir.actions.act_window">
    <field name="name">${Nama Object dalam bentuk plural}</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">${name_object}</field>
    <field name="view_mode">tree,form</field>
</record>
```

7. Buatkan satu menuitem dengan format:

```xml
<menuitem
  id="${name_object}_menu"
  name="Classes"
  action="${XML ID dari E.8.6}"
  groups="${XML ID dari E.2.1.1}"
  parent="${berikan plaholder saja}"
/>
```

### E.9 Ketentuan Attribute-attribute Wajib

Buatkan attribute-attribute:

```python
# mixin.multiple_approval attributes
_approval_from_state = "draft"
_approval_to_state = "done"
_approval_state = "confirm"
_after_approved_method = "action_done"

# Attributes related to add element on view automatically
_automatically_insert_view_element = True
_automatically_insert_done_button = False
_automatically_insert_done_policy_fields = False

# Attributes related to add element on form view automatically
_statusbar_visible_label = "draft,confirm,done"
_policy_field_order = [
    "confirm_ok",
    "approve_ok",
    "reject_ok",
    "restart_approval_ok",
    "done_ok",
    "cancel_ok",
    "restart_ok",
    "manual_number_ok",
]
_header_button_order = [
    "action_confirm",
    "action_approve",
    "action_reject",
    "action_done",
    "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
    "action_restart",
    "action_recompute_all_fields",
]

# Attributes related to add element on search view automatically
_state_filter_order = [
    "dom_draft",
    "dom_confirm",
    "dom_done",
    "dom_cancel",
    "dom_terminate",
    "dom_reject",
]

# Sequence attribute
_create_sequence_state = "done"


```

### E.10 Import Decorator

Tambahkan import sebagai berikut:

```python
from odoo.addons.ssi_decorator import ssi_decorator

```

### E.11 Method \_insert_form_element

Tambahkan method sebagai berikut:

```python
@ssi_decorator.insert_on_form_view()
def _insert_form_element(self, view_arch):
    if self._automatically_insert_view_element:
        view_arch = self._reconfigure_statusbar_visible(view_arch)
    return view_arch
```

### E.12 Method \_get_policy_field

Tambahkan method sebagai berikut:

```python
@api.model
def _get_policy_field(self):
    res = super()._get_policy_field()
    policy_field = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "reject_ok",
        "manual_number_ok",
        "restart_approval_ok",
    ]
    res += policy_field
    return res
```
