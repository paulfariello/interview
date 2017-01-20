def configure(ctx):
    ctx.env.INTERVIEW_PREFIX = ctx.env.PREFIX + '/share/interview'
    ctx.env.SERVER_PATH = ctx.env.INTERVIEW_PREFIX + '/server'
    ctx.env.STATIC_PATH = ctx.env.INTERVIEW_PREFIX + '/static'
    ctx.recurse('server')
    ctx.recurse('client')


def build(ctx):
    ctx.recurse('server')
    #ctx.recurse('client')
