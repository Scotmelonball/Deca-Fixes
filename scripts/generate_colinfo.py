import os
import io
import re
from deca.vfs_db import vfs_structure_open
from deca.file import ArchiveFile
from deca.ff_adf import adf_node_read

do_description = True


def process_translation_adf(vfs, f, sz):
    buffer = f.read(sz)
    adf = vfs.adf_db.load_adf(buffer)

    txt_buffer = adf.table_instance_values[0]['Text']
    txt_buffer = [(t + 256) % 256 for t in txt_buffer]
    txt_buffer = bytearray(txt_buffer)

    tr = {}
    with ArchiveFile(io.BytesIO(txt_buffer)) as tf:
        for prs in adf.table_instance_values[0]['SortedPairs']:
            tf.seek(prs['TextOffset'])
            text = tf.read_strz().decode('utf-8')
            tf.seek(prs['NameOffset'])
            name = tf.read_strz().decode('utf-8')
            tr[name] = text

    if os.path.exists(os.path.join('scratch', 'gz')):
        with open(os.path.join('scratch', 'gz', 'text_debug.txt'), 'w') as dt:
            for k, v in tr.items():
                dt.write('{}\t{}\n'.format(k, v.replace('\n', '<br>')))

    return tr


vfs = vfs_structure_open('/home/krys/prj/work/gz/project.json')

# load translation
vnode = vfs.map_vpath_to_vfsnodes[b'text/master_eng.stringlookup'][0]
with vfs.file_obj_from(vnode, 'rb') as f:
    tr = process_translation_adf(vfs, f, vnode.size_u)

# LOAD from global/collection.collectionc
# todo dump of different vnodes, one in gdcc is stripped
vnode = vfs.map_vpath_to_vfsnodes[b'global/collection.collectionc'][0]
adf = adf_node_read(vfs, vnode)

collectable_info = [
    (re.compile(r'collectable_dalahast_(.*)'), 'collectable_dalahast_{}',  'collectable_dalahast_{}_desc', True),
    (re.compile(r'collectable_gnome_(.*)'), 'collectable_gnome_{}',  'collectable_gnome_{}_desc', True),
    (re.compile(r'collectable_mixtape_(.*)'), 'collectable_mixtape_{}_name',  'collectable_mixtape_{}_desc', True),
    (re.compile(r'collectable_blueprint_(.*)'), 'collectable_blueprint_{}',  'collectable_blueprint_{}_desc', True),
    (re.compile(r'collectable_location_(.*)'), 'collectable_location_{}',  'collectable_location_{}_desc', False),
    (re.compile(r'dlc01_collectable_mixtape_([0-9]*)_.*'), 'collectable_lore_{}_.*_name',  'island01_collectable_mixtape_{}_.*_desc', True),
    (re.compile(r'collectable_biography_([0-9]*)_.*'), '^collectable_biography_{}_.*$(?<!_desc)',  'collectable_biography_{}_.*_desc', True),
    (re.compile(r'collectable_photo_(.*)'), 'collectable_photo_{}',  'collectable_photo_{}_desc', True),
    ]

collectables = []
for v in adf.table_instance_values[0]['Collectibles']:
    obj_id = v['ID']
    cid = v['Name'].decode('utf-8')

    name = None
    desc = None
    for ci in collectable_info:
        mv = ci[0].match(cid)
        if mv is not None:
            name = ci[1].format(mv.group(1))
            desc = ci[2].format(mv.group(1))
            break

    if name is None:
        print(cid)
    else:
        if name not in tr:
            rx = re.compile(name)
            for k in tr.keys():
                if rx.match(k) is not None:
                    name = k
                    break

        if desc not in tr:
            rx = re.compile(desc)
            for k in tr.keys():
                if rx.match(k) is not None:
                    desc = k
                    break

        name = tr[name]
        desc = tr[desc]
        position = v['Position']

        obj = {
            'type': 'Feature',
            'properties': {
                'type': 'collection.collectionc',
                'uid': obj_id,
                'uid_str': '0x{:012X}'.format(obj_id),
                'collectable_id': cid,
                'collectable_name_tr': name,
                'collectable_desc_tr': desc,
                'position': position,
            },
        }
        collectables.append(obj)

for ci in collectable_info:
    ex = ci[0]
    do_location = ci[-1]
    sd = {}
    for c in collectables:
        props = c['properties']
        if ex.match(props['collectable_id']) is not None:
            sd[props['collectable_id']] = [props['collectable_name_tr'], props['collectable_desc_tr'], props['position']]

    sn = list(sd.keys())
    sn.sort()

    print()
    print('{| class = "article-table"')
    print('!Name')
    if do_description:
        print('!Description')
    if do_location:
        print('!Location')
    for n in sn:
        desc = sd[n][1]
        desc = desc.replace('\n', '<br/>')
        desc = desc.replace('|', ' ')
        print('|-')
        print('|{}'.format(sd[n][0]))
        if do_description:
            print('|{}'.format(desc))
        if do_location:
            print('| {:.1f}, {:.1f}'.format(sd[n][2][0], sd[n][2][2]))
    print('|}')
