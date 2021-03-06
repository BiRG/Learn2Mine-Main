from datetime import datetime

from boto.resultset import ResultSet

class Stack:
    def __init__(self, connection=None):
        self.connection = connection
        self.creation_time = None
        self.description = None
        self.disable_rollback = None
        self.notification_arns = []
        self.outputs = []
        self.parameters = []
        self.capabilities = []
        self.stack_id = None
        self.stack_status = None
        self.stack_name = None
        self.stack_name_reason = None
        self.timeout_in_minutes = None

    def startElement(self, name, attrs, connection):
        if name == "Parameters":
            self.parameters = ResultSet([('member', Parameter)])
            return self.parameters
        elif name == "Outputs":
            self.outputs = ResultSet([('member', Output)])
            return self.outputs
        elif name == "Capabilities":
            self.capabilities = ResultSet([('member', Capability)])
            return self.capabilities
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'CreationTime':
            self.creation_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        elif name == "Description":
            self.description = value
        elif name == "DisableRollback":
            self.disable_rollback = bool(value)
        elif name == "NotificationARNs":
            self.notification_arns = value
        elif name == 'StackId':
            self.stack_id = value
        elif name == 'StackName':
            self.stack_name = value
        elif name == 'StackStatus':
            self.stack_status = value
        elif name == "StackStatusReason":
            self.stack_status_reason = value
        elif name == "TimeoutInMinutes":
            self.timeout_in_minutes = int(value)
        elif name == "member":
            pass
        else:
            setattr(self, name, value)

    def delete(self):
        return self.connection.delete_stack(stack_name_or_id=self.stack_id)

    def describe_events(self, next_token=None):
        return self.connection.describe_stack_events(
            stack_name_or_id=self.stack_id,
            next_token=next_token
        )

    def describe_resource(self, logical_resource_id):
        return self.connection.describe_stack_resource(
            stack_name_or_id=self.stack_id,
            logical_resource_id=logical_resource_id
        )

    def describe_resources(self, logical_resource_id=None,
            physical_resource_id=None):
        return self.connection.describe_stack_resources(
            stack_name_or_id=self.stack_id,
            logical_resource_id=logical_resource_id,
            physical_resource_id=physical_resource_id
        )

    def list_resources(self, next_token=None):
        return self.connection.list_stack_resources(
            stack_name_or_id=self.stack_id,
            next_token=next_token
        )

    def update(self):
        rs = self.connection.describe_stacks(self.stack_id)
        if len(rs) == 1 and rs[0].stack_id == self.stack_id:
            self.__dict__.update(rs[0].__dict__)
        else:
            raise ValueError("%s is not a valid Stack ID or Name" %
                self.stack_id)

    def get_template(self):
        return self.connection.get_template(stack_name_or_id=self.stack_id)

class StackSummary:
    def __init__(self, connection=None):
        self.connection = connection
        self.stack_id = None
        self.stack_status = None
        self.stack_name = None
        self.creation_time = None
        self.deletion_time = None
        self.template_description = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'StackId':
            self.stack_id = value
        elif name == 'StackStatus':
            self.stack_status = value
        elif name == 'StackName':
            self.stack_name = value
        elif name == 'CreationTime':
            self.creation_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        elif name == "DeletionTime":
            self.deletion_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        elif name == 'TemplateDescription':
            self.template_description = value
        elif name == "member":
            pass
        else:
            setattr(self, name, value)

class Parameter:
    def __init__(self, connection=None):
        self.connection = None
        self.key = None
        self.value = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == "ParameterKey":
            self.key = value
        elif name == "ParameterValue":
            self.value = value
        else:
            setattr(self, name, value)

    def __repr__(self):
        return "Parameter:\"%s\"=\"%s\"" % (self.key, self.value)

class Output:
    def __init__(self, connection=None):
        self.connection = connection
        self.description = None
        self.key = None
        self.value = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == "Description":
            self.description = value
        elif name == "OutputKey":
            self.key = value
        elif name == "OutputValue":
            self.value = value
        else:
            setattr(self, name, value)

    def __repr__(self):
        return "Output:\"%s\"=\"%s\"" % (self.key, self.value)

class Capability:
    def __init__(self, connection=None):
        self.connection = None
        self.value = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        self.value = value

    def __repr__(self):
        return "Capability:\"%s\"" % (self.value)

class StackResource:
    def __init__(self, connection=None):
        self.connection = connection
        self.description = None
        self.logical_resource_id = None
        self.physical_resource_id = None
        self.resource_status = None
        self.resource_status_reason = None
        self.resource_type = None
        self.stack_id = None
        self.stack_name = None
        self.timestamp = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == "Description":
            self.description = value
        elif name == "LogicalResourceId":
            self.logical_resource_id = value
        elif name == "PhysicalResourceId":
            self.physical_resource_id = value
        elif name == "ResourceStatus":
            self.resource_status = value
        elif name == "ResourceStatusReason":
            self.resource_status_reason = value
        elif name == "ResourceType":
            self.resource_type = value
        elif name == "StackId":
            self.stack_id = value
        elif name == "StackName":
            self.stack_name = value
        elif name == "Timestamp":
            self.timestamp = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        else:
            setattr(self, name, value)

    def __repr__(self):
        return "StackResource:%s (%s)" % (self.logical_resource_id,
                self.resource_type)

class StackResourceSummary:
    def __init__(self, connection=None):
        self.connection = connection
        self.last_updated_timestamp = None
        self.logical_resource_id = None
        self.physical_resource_id = None
        self.resource_status = None
        self.resource_status_reason = None
        self.resource_type = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == "LastUpdatedTimestamp":
            self.last_updated_timestamp = datetime.strptime(value,
                '%Y-%m-%dT%H:%M:%SZ')
        elif name == "LogicalResourceId":
            self.logical_resource_id = value
        elif name == "PhysicalResourceId":
            self.physical_resource_id = value
        elif name == "ResourceStatus":
            self.resource_status = value
        elif name == "ResourceStatusReason":
            self.resource_status_reason = value
        elif name == "ResourceType":
            self.resource_type = value
        else:
            setattr(self, name, value)

    def __repr__(self):
        return "StackResourceSummary:%s (%s)" % (self.logical_resource_id,
                self.resource_type)

class StackEvent:
    valid_states = ("CREATE_IN_PROGRESS", "CREATE_FAILED", "CREATE_COMPLETE",
            "DELETE_IN_PROGRESS", "DELETE_FAILED", "DELETE_COMPLETE")
    def __init__(self, connection=None):
        self.connection = connection
        self.event_id = None
        self.logical_resource_id = None
        self.physical_resource_id = None
        self.resource_properties = None
        self.resource_status = None
        self.resource_status_reason = None
        self.resource_type = None
        self.stack_id = None
        self.stack_name = None
        self.timestamp = None

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == "EventId":
            self.event_id = value
        elif name == "LogicalResourceId":
            self.logical_resource_id = value
        elif name == "PhysicalResourceId":
            self.physical_resource_id = value
        elif name == "ResourceProperties":
            self.resource_properties = value
        elif name == "ResourceStatus":
            self.resource_status = value
        elif name == "ResourceStatusReason":
            self.resource_status_reason = value
        elif name == "ResourceType":
            self.resource_type = value
        elif name == "StackId":
            self.stack_id = value
        elif name == "StackName":
            self.stack_name = value
        elif name == "Timestamp":
            self.timestamp = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        else:
            setattr(self, name, value)

    def __repr__(self):
        return "StackEvent %s %s %s" % (self.resource_type,
                self.logical_resource_id, self.resource_status)
