"""init database

Revision ID: 340a716780a2
Revises: 
Create Date: 2019-09-05 11:51:24.274493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '340a716780a2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    entities = op.create_table(
        'entities',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('name', sa.String(256),),
        sa.Column('object', sa.String(256),),
        sa.Column('date_created', sa.DateTime,),
        sa.Column('paused', sa.Boolean,),

        sa.Column('declensions', sa.ARRAY(sa.String), server_default="{}"),

        # indices
        sa.PrimaryKeyConstraint('id', name='entity_pkey',),
    )

    link_types = op.create_table(
        'link_types',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('name', sa.String(256), nullable=False,),
        sa.Column('description', sa.String(256), nullable=False,),

        # indices
        sa.PrimaryKeyConstraint('id', name='link-type_pkey',),
    )

    links = op.create_table(
        'links',

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


    users = op.create_table(
        'users',

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

    permissions = op.create_table(
        'permissions',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('user_id', sa.Integer, nullable=False,),
        sa.Column('perm_name', sa.String(64), nullable=False,),

        # indices
        sa.PrimaryKeyConstraint('id', name='permission_pkey',),
        sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                                name='user_permission_fkey',
                                ondelete='CASCADE',),
    )

    label_types = op.create_table(
        'label_types',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('name', sa.String(256), nullable=False,),
        sa.Column('description', sa.String(256), nullable=False,),

        # indices
        sa.PrimaryKeyConstraint('id', name='label-type_pkey',),
    )

    labels = op.create_table(
        'labels',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('entity_id', sa.Integer, nullable=False,),
        sa.Column('parent_id', sa.Integer,),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('is_node', sa.Boolean,),
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

    countries = op.create_table(
        'countries',
        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('entity_id', sa.Integer, nullable=False,),

        sa.Column('name', sa.String(256),),

        # indices
        sa.PrimaryKeyConstraint('id', name='country_pkey',),
        sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                                name='entity_permission_fkey',
                                ondelete='CASCADE',),
    )

    manufacturers = op.create_table(
        'manufacturers',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('entity_id', sa.Integer, nullable=False,),
        sa.Column('parent_id', sa.Integer,),
        sa.Column('is_node', sa.Boolean,),

        sa.Column('country_id', sa.Integer,),
        sa.Column('name', sa.String(256),),

        # indices
        sa.PrimaryKeyConstraint('id', name='manufacturer_pkey',),
        sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                                name='entity_permission_fkey',
                                ondelete='CASCADE',),
        sa.ForeignKeyConstraint(['country_id'], [countries.c.id],
                                name='country_permission_fkey',
                                ondelete='CASCADE',),
    )

    products = op.create_table(
        'products',

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
    )

    offers = op.create_table(
        'offers',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('entity_id', sa.Integer, nullable=False,),
        sa.Column('parent_id', sa.Integer,),
        sa.Column('is_node', sa.Boolean,),

        sa.Column('name', sa.String(256),),
        sa.Column('weight', sa.Float,),
        sa.Column('price', sa.Float(precision=2),),
        sa.Column('count_type', sa.Integer),

        # indices
        sa.PrimaryKeyConstraint('id', name='offer_pkey',),
        sa.ForeignKeyConstraint(['entity_id'], [entities.c.id],
                                name='entity_permission_fkey',
                                ondelete='CASCADE',),
    )

    orders = op.create_table(
        'orders',

        sa.Column('id', sa.Integer, nullable=False,),
        sa.Column('entity_id', sa.Integer, nullable=False,),

        sa.Column('user_id', sa.Integer, nullable=False,),

        sa.Column('person_name', sa.String(256), nullable=False,),
        sa.Column('person_phone', sa.String(256), nullable=False,),
        sa.Column('person_address', sa.String(256), nullable=False,),
        sa.Column('person_email', sa.String(256),),

        sa.Column('delivery_date', sa.Date(), nullable=False,),
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

    messages = op.create_table(
        'messages',

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

def downgrade():
    op.drop_table('links')
    op.drop_table('link_types')
    op.drop_table('labels')
    op.drop_table('label_types')
    op.drop_table('offers')
    op.drop_table('orders')
    op.drop_table('manufacturers')
    op.drop_table('countries')
    op.drop_table('products')
    op.drop_table('messages')
    op.drop_table('permissions')
    op.drop_table('users')
    op.drop_table('entities')
