"""Initial migration.

Revision ID: a57d2b2f19f2
Revises: 
Create Date: 2021-01-19 13:32:54.786425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a57d2b2f19f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasets_v2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('type', sa.Enum('PSI', 'STREAMING', name='datasettype'), nullable=True),
    sa.Column('external_storage_path', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('job_dependency_v2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('src_job_id', sa.Integer(), nullable=True),
    sa.Column('dst_job_id', sa.Integer(), nullable=True),
    sa.Column('dep_index', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_dependency_v2_dst_job_id'), 'job_dependency_v2', ['dst_job_id'], unique=False)
    op.create_index(op.f('ix_job_dependency_v2_src_job_id'), 'job_dependency_v2', ['src_job_id'], unique=False)
    op.create_table('projects_v2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('config', sa.Text(), nullable=True),
    sa.Column('certificate', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_v2_name'), 'projects_v2', ['name'], unique=True)
    op.create_index(op.f('ix_projects_v2_token'), 'projects_v2', ['token'], unique=False)
    op.create_table('template_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('group_alias', sa.String(length=255), nullable=False),
    sa.Column('config', sa.Text(), nullable=False),
    sa.Column('is_left', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_template_v2_group_alias'), 'template_v2', ['group_alias'], unique=False)
    op.create_index(op.f('ix_template_v2_name'), 'template_v2', ['name'], unique=True)
    op.create_table('users_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_v2_username'), 'users_v2', ['username'], unique=False)
    op.create_table('data_batches_v2',
    sa.Column('event_time', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.Enum('SUCCESS', 'FAILED', 'IMPORTING', name='batchstate'), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.Column('failed_source', sa.Text(), nullable=True),
    sa.Column('file_size', sa.Integer(), nullable=True),
    sa.Column('imported_file_num', sa.Integer(), nullable=True),
    sa.Column('num_file', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets_v2.id'], ),
    sa.PrimaryKeyConstraint('event_time', 'dataset_id')
    )
    op.create_table('workflow_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('config', sa.Text(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('forkable', sa.Boolean(), nullable=True),
    sa.Column('forked_from', sa.Integer(), nullable=True),
    sa.Column('forked_job_indices', sa.TEXT(), nullable=True),
    sa.Column('recur_type', sa.Enum('NONE', 'ON_NEW_DATA', 'HOURLY', 'DAILY', 'WEEKLY', name='recurtype'), nullable=True),
    sa.Column('recur_at', sa.Interval(), nullable=True),
    sa.Column('trigger_dataset', sa.Integer(), nullable=True),
    sa.Column('last_triggered_batch', sa.Integer(), nullable=True),
    sa.Column('job_ids', sa.TEXT(), nullable=True),
    sa.Column('state', sa.Enum('INVALID', 'NEW', 'READY', 'RUNNING', 'STOPPED', name='workflowstate'), nullable=True),
    sa.Column('target_state', sa.Enum('INVALID', 'NEW', 'READY', 'RUNNING', 'STOPPED', name='workflowstate'), nullable=True),
    sa.Column('transaction_state', sa.Enum('READY', 'ABORTED', 'COORDINATOR_PREPARE', 'COORDINATOR_COMMITTABLE', 'COORDINATOR_COMMITTING', 'COORDINATOR_ABORTING', 'PARTICIPANT_PREPARE', 'PARTICIPANT_COMMITTABLE', 'PARTICIPANT_COMMITTING', 'PARTICIPANT_ABORTING', name='transactionstate'), nullable=True),
    sa.Column('transaction_err', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects_v2.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_v2_name'), 'workflow_v2', ['name'], unique=True)
    op.create_table('job_v2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('job_type', sa.Enum('UNSPECIFIED', 'RAW_DATA', 'DATA_JOIN', 'PSI_DATA_JOIN', 'NN_MODEL_TRANINING', 'TREE_MODEL_TRAINING', 'NN_MODEL_EVALUATION', 'TREE_MODEL_EVALUATION', name='jobtype'), nullable=False),
    sa.Column('state', sa.Enum('INVALID', 'STOPPED', 'WAITING', 'STARTED', name='jobstate'), nullable=False),
    sa.Column('yaml', sa.Text(), nullable=False),
    sa.Column('config', sa.Text(), nullable=False),
    sa.Column('workflow_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('flapp_snapshot', sa.Text(), nullable=True),
    sa.Column('pods_snapshot', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects_v2.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow_v2.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_job_v2_workflow_id'), 'job_v2', ['workflow_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_job_v2_workflow_id'), table_name='job_v2')
    op.drop_table('job_v2')
    op.drop_index(op.f('ix_workflow_v2_name'), table_name='workflow_v2')
    op.drop_table('workflow_v2')
    op.drop_table('data_batches_v2')
    op.drop_index(op.f('ix_users_v2_username'), table_name='users_v2')
    op.drop_table('users_v2')
    op.drop_index(op.f('ix_template_v2_name'), table_name='template_v2')
    op.drop_index(op.f('ix_template_v2_group_alias'), table_name='template_v2')
    op.drop_table('template_v2')
    op.drop_index(op.f('ix_projects_v2_token'), table_name='projects_v2')
    op.drop_index(op.f('ix_projects_v2_name'), table_name='projects_v2')
    op.drop_table('projects_v2')
    op.drop_index(op.f('ix_job_dependency_v2_src_job_id'), table_name='job_dependency_v2')
    op.drop_index(op.f('ix_job_dependency_v2_dst_job_id'), table_name='job_dependency_v2')
    op.drop_table('job_dependency_v2')
    op.drop_table('datasets_v2')
    # ### end Alembic commands ###
