def function(*args):
    print(args, type(args))

function(1,2)


def function(x, y, *args):
    '''

    asdasdasd

    :param x:
    :param y:
    :param args:
    :return:
    '''
    print(x, y, args)

function(1, 2, 3, 4, 5)

def function(**kwargs):
    print(kwargs, type(kwargs))

function(a=2,b=3,c=4)

def function(arg,*args,**kwargs):
    print(arg,args,kwargs)

function(6,7,8,9,a=1, b=2, c=3)