# -*- coding: utf-8 -*-


STYLE = {
        'fore':
        {   # fore
            'black'    : 30,   
            'red'      : 31,   
            'green'    : 32,   
            'yellow'   : 33,   
            'blue'     : 34,   
            'purple'   : 35,   
            'cyan'     : 36,   
            'white'    : 37,   
        },

        'back' :
        {   # back
            'black'     : 40,  
            'red'       : 41,  
            'green'     : 42,  
            'yellow'    : 43,  
            'blue'      : 44,  
            'purple'    : 45, 
            'cyan'      : 46,  
            'white'     : 47,  
        },

        'mode' :
        {   # mode
            'mormal'    : 0,   #  default
            'bold'      : 1,   
            'underline' : 4,   
            'blink'     : 5,   
            'invert'    : 7,   
            'hide'      : 8,   
        },

        'default' :
        {
            'end' : 0,
        },
}


def UseStyle(string, mode = '', fore = '', back = ''):

    mode  = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''

    fore  = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''

    back  = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''

    style = ';'.join([s for s in [mode, fore, back] if s])

    style = '\033[%sm' % style if style else ''

    end   = '\033[%sm' % STYLE['default']['end'] if style else ''

    return '%s%s%s' % (style, string, end)


def TestColor( ):

    print (UseStyle('normal display'))
    print ('')

    print("test mode")
    print (UseStyle('bold',   mode = 'bold')),
    print (UseStyle('underline', mode = 'underline')),
    print (UseStyle('blink',   mode = 'blink')),
    print (UseStyle('invert',   mode = 'invert')),
    print (UseStyle('hide', mode = 'hide'))
    print ('')

    print ("test fore")
    print (UseStyle('black',   fore = 'black')),
    print (UseStyle('red',   fore = 'red')),
    print (UseStyle('green',   fore = 'green')),
    print (UseStyle('yellow',   fore = 'yellow')),
    print (UseStyle('blue',   fore = 'blue')),
    print (UseStyle('purple', fore = 'purple')),
    print (UseStyle('cyan', fore = 'cyan')),
    print (UseStyle('white',   fore = 'white'))
    print ('')

    print ("test back")
    print (UseStyle('black',   back = 'black')),
    print (UseStyle('red',   back = 'red')),
    print (UseStyle('green',   back = 'green')),
    print (UseStyle('yellow',   back = 'yellow')),
    print (UseStyle('blue',   back = 'blue')),
    print (UseStyle('purple', back = 'purple')),
    print (UseStyle('cyan', back = 'cyan')),
    print (UseStyle('white',   back = 'white')),
    print ('')


if __name__ == '__main__':
    TestColor( )

