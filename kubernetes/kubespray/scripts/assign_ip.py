from cloudify import ctx


ctx.instance.runtime_properties['cloudify_agent'] = dict()
ctx.instance.runtime_properties['cloudify_agent']['ip'] = ctx.instance.runtime_properties['reservation']
ctx.instance.runtime_properties['cloudify_agent']['ip'] = ctx.instance.runtime_properties['reservation']

ctx.instance.runtime_properties['ip'] = ctx.instance.runtime_properties['reservation']

