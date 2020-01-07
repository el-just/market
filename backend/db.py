import sqlalchemy as sa
import enum


metadata = sa.MetaData()

settings = sa.Table(
    'settings', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('name', sa.String(256),),
    sa.Column('value', sa.String(256),),

    # indices
    sa.PrimaryKeyConstraint('id', name='setting_pkey',),
)

entities = sa.Table(
    'entities', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('name', sa.String(256),),
    sa.Column('object', sa.String(256),),
    sa.Column('date_created', sa.DateTime, nullable=False,),
    sa.Column('paused', sa.Boolean,),

    sa.Column('declensions', sa.ARRAY(sa.String), server_default="{}"),

    # indices
    sa.PrimaryKeyConstraint('id', name='entity_pkey',),
)

link_types = sa.Table(
    'link_types', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('name', sa.String(256), nullable=False,),
    sa.Column('description', sa.String(256), nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='link-type_pkey',),
)

links = sa.Table(
    'links', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('object_id', sa.Integer, nullable=False,),
    sa.Column('subject_id', sa.Integer, nullable=False,),
    sa.Column('type_id', sa.Integer, nullable=False,),

    sa.Column('weight', sa.Float,),
    sa.Column('multiplier', sa.Float,),

    # indices
    sa.PrimaryKeyConstraint('id', name='link_pkey',),

    sa.ForeignKeyConstraint(['object_id'], [entities.c.id],
                            name='object_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['subject_id'], [entities.c.id],
                            name='subject_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['type_id'], [link_types.c.id],
                            name='type_permission_fkey',
                            ondelete='CASCADE',),
)

users = sa.Table(
    'users', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('login', sa.String(256), nullable=False,),
    sa.Column('passwd', sa.String(256), nullable=False,),
    sa.Column('is_superuser', sa.Boolean, nullable=False,
              server_default='FALSE',),

    sa.Column('entity_id', sa.Integer, nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='user_pkey',),
    sa.UniqueConstraint('login', name='user_login_key',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
)

permissions = sa.Table(
    'permissions', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('user_id', sa.Integer, nullable=False,),
    sa.Column('perm_name', sa.String(64), nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='permission_pkey',),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE',),
)

label_types = sa.Table(
    'label_types', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('name', sa.String(256), nullable=False,),
    sa.Column('description', sa.String(256), nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='label-type_pkey',),
)

labels = sa.Table(
    'labels', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),
    sa.Column('parent_id', sa.Integer,),
    sa.Column('is_node', sa.Boolean,),
    sa.Column('name', sa.String(256), nullable=False),

    sa.Column('type_id', sa.Integer, nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='label_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['type_id'], [label_types.c.id],
                            name='type_permission_fkey',
                            ondelete='CASCADE',),
)

countries = sa.Table(
    'countries', metadata,
    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),

    sa.Column('name', sa.String(256),),

    # indices
    sa.PrimaryKeyConstraint('id', name='product_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
)

manufacturers = sa.Table(
    'manufacturers', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),
    sa.Column('parent_id', sa.Integer,),
    sa.Column('is_node', sa.Boolean,),

    sa.Column('country_id', sa.Integer,),
    sa.Column('name', sa.String(256),),

    # indices
    sa.PrimaryKeyConstraint('id', name='product_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['country_id'], [countries.c.id],
                            name='country_permission_fkey',
                            ondelete='CASCADE',),
)

products = sa.Table(
    'products', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),

    sa.Column('manufacturer_id', sa.Integer,),

    sa.Column('name', sa.String(256),),
    sa.Column('description', sa.String(256),),
    sa.Column('img', sa.String(256),),

    # indices
    sa.PrimaryKeyConstraint('id', name='product_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['manufacturer_id'], [manufacturers.c.id],
                            name='manufacturer_permission_fkey',
                            ondelete='CASCADE',),
)

offers = sa.Table(
    'offers', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),
    sa.Column('parent_id', sa.Integer,),
    sa.Column('is_node', sa.Boolean,),

    sa.Column('name', sa.String(256),),
    sa.Column('weight', sa.Float,),
    sa.Column('price', sa.Float(precision=2),),
    sa.Column('count_type', sa.Integer,),
    sa.Column('priority', sa.Integer,),

    # indices
    sa.PrimaryKeyConstraint('id', name='offer_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
)

orders = sa.Table(
    'orders', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),

    sa.Column('user_id', sa.Integer, nullable=False,),

    sa.Column('person_name', sa.String(256), nullable=False,),
    sa.Column('person_phone', sa.String(256), nullable=False,),
    sa.Column('person_address', sa.String(256), nullable=False,),
    sa.Column('person_email', sa.String(256),),

    sa.Column('delivery_date', sa.Date, nullable=False,),
    sa.Column('delivery_interval', sa.Integer, nullable=False,),
    sa.Column('payment_type', sa.Integer, nullable=False,),

    sa.Column('change_from', sa.Float,),
    sa.Column('extra_flags', sa.ARRAY(sa.Boolean),),

    sa.Column('special_instructions', sa.String(1024),),

    sa.Column('status', sa.Integer, nullable=False,),

    sa.Column('amount', sa.Float, nullable=False,),
    sa.Column('weight', sa.Float, nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='order_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE',),
)

messages = sa.Table(
    'messages', metadata,

    sa.Column('id', sa.Integer, nullable=False,),
    sa.Column('entity_id', sa.Integer, nullable=False,),

    sa.Column('email', sa.String(256),),
    sa.Column('user_id', sa.Integer,),
    sa.Column('message', sa.String,),

    sa.Column('status', sa.Integer, nullable=False,),

    # indices
    sa.PrimaryKeyConstraint('id', name='message_pkey',),
    sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                            name='entity_permission_fkey',
                            ondelete='CASCADE',),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE',),
)
