from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from random import randint

def home(request):
    return render(request, 'symmetric_ciphers/home.html')

def stream(request):
    return render(request, 'symmetric_ciphers/stream.html')

def ceaser(request):
    return render(request, 'symmetric_ciphers/ceaser.html')

def ceaser_exicute(request):
    ip =  request.POST.get('input') 
    key = int(request.POST.get('key')) 
    encryption = request.POST.get('encryption')
    output = ''
    if(encryption == 'true'):
        for i in ip:
            if i.isspace():
                output += ' '
            elif i.islower():
                output += chr((((ord(i)-97) + key) % 26) + 97)
            else:
                output += chr((((ord(i)-65) + key) % 26) + 65)
    else:
        for i in ip:
            if i.isspace():
                output += ' '
            elif i.islower():
                output += chr(((((ord(i)-97) - key) + 26) % 26) + 97)
            else:
                output += chr(((((ord(i)-65) - key) + 26)% 26) + 65)
    result = {
        'output': output
        }
    return JsonResponse(result)

def monoalphabetic(request):
    return render(request, 'symmetric_ciphers/monoalphabetic.html')

def monoalphabetic_exicute(request):
    ip =  request.POST.get('input')
    ip = ip.lower()
    encryption = request.POST.get('encryption')

    count = {'a':'m', 'b':'n', 'c':'b', 'd':'v', 'e':'c', 'f':'x', 'g':'z', 'h':'l', 'i':'k', 'j':'j', 'k':'h', 'l':'g', 'm':'f', 'n':'d', 'o':'s', 'p':'a', 'q':'p', 'r':'o', 's':'i', 't':'u', 'u':'y', 'v':'t', 'w':'r', 'x':'e', 'y':'w', 'z':'q'}
    output = ''

    if(encryption == 'true'):
        for i in ip:
            if i.isspace():
                output += ' '
                continue
            output += (count[i])
    else:
        keys = list(count)
        values = list(count.values())
        for i in ip:
            if i.isspace():
                output += ' '
                continue
            output += keys[values.index(i)]
    result = {
        'output': output
        }
    return JsonResponse(result)

def polyalphabetic(request):
    return render(request, 'symmetric_ciphers/polyalphabetic.html')

def polyalphabetic_exicute(request):
    ip =  request.POST.get('input')
    key = request.POST.get('key')
    key = key.lower()
    encryption = request.POST.get('encryption')

    output = ''

    if(encryption == 'true'):
        for i in range(len(ip)):
            if ip[i].isspace():
                output += ip[i]
                continue
            if ip[i].islower():
                n = 97
            elif ip[i].isupper():
                n = 65
            else:
                n = 100
            #---------------------
            p = ord( ip[i] ) - n
            k = ord( key[i % len(key)] ) - n
            output += chr( ( p+k )%26 + n )
    else:
        for i in range(len(ip)):
            if ip[i].isspace():
                output += ip[i]
                continue
            if ip[i].islower():
                n = 97
            elif ip[i].isupper():
                n = 65
            else:
                n = 100
        #---------------------
            c = ord( ip[i] ) - n
            k = ord( key[i % len(key)] ) - n
            output += chr( ( c-k+26 )%26 + n )
    
    
    result = {
        'output': output
        }
    return JsonResponse(result)

def hill(request):
    return render(request, 'symmetric_ciphers/hill.html')

def hill_exicute(request):
    ip =  request.POST.get('input') 
    key = request.POST.get('key')
    matrix_size = int( request.POST.get('matrix_size') )
    encryption = request.POST.get('encryption')
    
    details = []
    output = ''

    n = matrix_size


    def key_inverse(di, matrix, size):
        ki = matrix.copy()
        for i in range(size):
            for j in range(size):
                ki[i][j] = ( matrix[i][j]*di ) % 26
        return ki

    def adjoint(matrix, size):
        adj = matrix.copy()
        if size == 2:
            adj[0][0], adj[1][1] = adj[1][1], adj[0][0]
            adj[0][1] *= -1
            adj[1][0] *= -1
        elif size == 3:
            temp = []
            temp.append(adj[1][1]*adj[2][2]-adj[2][1]*adj[1][2])#A1
            temp.append(adj[1][2]*adj[2][0]-adj[1][0]*adj[2][2])#A2
            temp.append(adj[1][0]*adj[2][1]-adj[2][0]*adj[1][1])#A3
            temp.append(adj[0][2]*adj[2][1]-adj[0][1]*adj[2][2])#A4
            temp.append(adj[0][0]*adj[2][2]-adj[0][2]*adj[2][0])#A5
            temp.append(adj[0][1]*adj[2][0]-adj[0][0]*adj[2][1])#A6
            temp.append(adj[0][1]*adj[1][2]-adj[0][2]*adj[1][1])#A7
            temp.append(adj[0][2]*adj[1][0]-adj[0][0]*adj[1][2])#A8
            temp.append(adj[0][0]*adj[1][1]-adj[0][1]*adj[1][0])#A9
            
            val  = 0
            for i in range(3):
                for j in range(3):
                    adj[i][j] = temp[val]%26
                    val += 1
            #swap------
            adj[0][1], adj[1][0] = adj[1][0],  adj[0][1]
            adj[0][2], adj[2][0] = adj[2][0],  adj[0][2]
            adj[2][1], adj[1][2] = adj[1][2],  adj[2][1]
        return adj

    def dinverse(d):
        nonlocal details

        if ( d == 0 or d == 13 or d%2 == 0 ):
            print("For inverse, Determinent not allowed to be 0 or 13 or even !!")
            details.append("For inverse, Determinent not allowed to be 0 or 13 or even !!")
            return
        di = val = 0
        while(val != 1):
            di += 1
            val = (d * di)%26
        return di

    def change_char(m):
        ct = ''
        for i in range(len(m)):
            for j in range(len(m[0])):
                for k in range(len(m[i][j])):
                    ct+= chr( m[i][j][k] + 97)
        return ct
    
    def mul(X, Y):
        ct_matrix = [[0]*len(Y[0]) for i in range(len(Y))]
        for i in range(len(X)):
            for j in range(len(Y[0])):
                for k in range(len(Y)):
                    ct_matrix[i][j] += X[i][k] * Y[k][j]
                ct_matrix[i][j] %= 26
        return ct_matrix

    def gram(s, n):
        nonlocal details

        list_gram = []
        if n == 2:
            if (len(s)%2 !=0 ):
                s +=  'a'
        elif n == 3:
            if (len(s)%3 !=0 ):
                s += 'a'
                if(len(s)%3 != 0):
                    s += 'a'
        for i in range(0, len(s), n):
            temp_list = []
            if n == 2:
                string = s[i]+s[i+1]
            elif n == 3:
                string = s[i]+s[i+1]+s[i+2]
            l = list(string)
            for i in range(len(l)):
                temp_list.append(list(l[i]))
            list_gram.append(temp_list)

        print("PlainText :", list_gram)
        details.append("PlainText: " + str(list_gram))

        num_list_gram = list_gram
        for i in range(len(list_gram)):
            for j in range(len(list_gram[i])):
                for k in range(len(list_gram[i][j])):
                    num_list_gram[i][j][k] = ord(list_gram[i][j][k].lower())-97
        return num_list_gram

    def wrong_key(key):
        nonlocal details

        f_char = ord(key[0].lower())-97
        try:
            s_char = ord(key[1].lower())-97
        except:
            s_char = 1
        try:
            t_char = ord(key[2].lower())-97
        except:
            t_char = 1
        if((f_char % 2 == 0) and (s_char % 2 == 0) and (t_char % 2 == 0)):

            print("First row charaters of key_matrix are even !!")
            details.append("First row charaters of key_matrix are even !!")
            print("Key not allowed !!")
            details.append("Key not allowed !!")

            return True
        return False
    #-------------------------------------------------------------------------------
    def key_mat(s, n, start):
        #---------------------
        temp = []
        for i in s:
            if i.islower():
                num = 97
            else:
                num = 65
            temp.append(ord(i)-num)
        #---------------------       
        for i in range(start, 200):
            if i < 26:
                temp.append(i)
            else:
                temp.append(randint(0, 25))
        #---------------------
        l = [[i]*n for i in range(n)]
        val = 0
        for i in range(n):
            for j in range(n):
                if val == len(temp):
                    return None
                l[i][j] = temp[val]
                val+=1
        return l
    #--------------------
    def determinant(matrix, size):
        if size==2:
            d = ((matrix[0][0]*matrix[1][1]) - (matrix[0][1]*matrix[1][0]))
        elif size == 3:
            d = (matrix[0][0]*matrix[1][1]*matrix[2][2] + matrix[0][1]*matrix[1][2]*matrix[2][0] + matrix[0][2]*matrix[1][0]*matrix[2][1] - matrix[0][2]*matrix[1][1]*matrix[2][0] - matrix[0][1]*matrix[1][0]*matrix[2][2] - matrix[0][0]*matrix[1][2]*matrix[2][1])
        return ((d+26) % 26)
    #------------------------------------------------------------------------
    def E(key_matrix, n):
        nonlocal details
        nonlocal output

        decr_key = ''
        for i in range(n):
            for j in range(n):
                decr_key += chr( key_matrix[i][j] + 97 )
        print("NOTE YOUR DECRYPTION KEY: ", decr_key)
        details.append("NOTE YOUR DECRYPTION KEY: " +  decr_key)

        pt = ip
        pt_matrix = gram(pt, n)
        print("Plain Text Matrix: ", pt_matrix)
        details.append("Plain Text Matrix: " + str(pt_matrix))

        ct_matrix = []
        for i in range(len(pt_matrix)):
            ct_matrix.append( mul(key_matrix, pt_matrix[i]) )
        print("Multiplication is: ", ct_matrix)
        details.append("Multiplication is: " + str(ct_matrix))
        ct_text = change_char(ct_matrix)
        print("Encrypted text: ", ct_text)
        output += str(ct_text)
        return ct_text, key_matrix

    def D(d, key_matrix, n):
        nonlocal details
        nonlocal output

        di = dinverse(d)
        print("DInverse: ", di)
        details.append("DInverse: " + str(di))
        adj = adjoint(key_matrix, n)
        print("Adjoint of key matrix: ", adj)
        details.append("Adjoint of key matrix: " + str(adj))
        ki = key_inverse(di, adj, n)
        print("Key Inverse: ", ki)
        details.append("Key Inverse: " + str(ki))
        ct = ip
        ct_matrix = gram(ct, n)
        pt_matrix = []
        for i in range(len(ct_matrix)):
            pt_matrix.append( mul(key_matrix, ct_matrix[i]) )
        print("Multiplication is: ", pt_matrix)
        details.append("Multiplication is: "+ str(pt_matrix))
        pt_text = change_char(pt_matrix)
        print("Decrypted text: ", pt_text)
        output += str(pt_text)

    if  ( wrong_key(key) ):
        result = {
            'details': details,
            'output': output
        }
        return JsonResponse(result)

    if( (n == 2 and len(key) >= 4) or ((n == 3) and len(key) >= 9) ):
        key_matrix = key_mat(key, n, 0)
        d = determinant(key_matrix, n)
        if (d == 0 or d == 13 or d%2 == 0):
            print(f"Determinant: {d}, which is 0 or 13 or even  !!")
            details.append("Determinant " + str(d) + " which is 0 or 13 or even  !!")
            details.append(" Key not allowed !!")
            print("Key not allowed !!")

            result = {
                'details': details,
                'output': output
            }
            return JsonResponse(result)
    
    else:
        try:
            start = 0
            while(True):
                key_matrix = key_mat(key, n, start)
                if not key_matrix:
                    key_matrix = key_mat(key, n, start)
                d = determinant(key_matrix, n)
                if (d != 0 and d != 13 and d%2 != 0):
                    break
                start += 1
        except:
            print("No matrix genrated for given key.")
            details.append("No matrix genrated for given key.")
            details.append("Key not allowed !!")
            print("Key not allowed !!")
            
            result = {
                'details': details,
                'output': output
            }
            return JsonResponse(result)
    
    print("Key_Matrix: ", key_matrix)
    details.append("Key_Matrix: " + str(key_matrix))
    print("Determinant: ", d)
    details.append("Determinant: " + str(d))

    if (encryption == 'true'):
        E(key_matrix, n)
    
    else:
        D(d, key_matrix, n)
    
    result = {
    'details': details,
    'output': output
    }
    return JsonResponse(result)

def playfair(request):
    return render(request, 'symmetric_ciphers/playfair.html')

def playfair_exicute(request):
    ip =  request.POST.get('input')
    print(ip)
    key = request.POST.get('key')
    encryption = request.POST.get('encryption')
    
    details = []
    output = ''
    output2 = ''

    def key_matrix(s):
        n = 5
        l = [[None]*n for i in range(n)]
        
        temp = []
        for i in s:
            if i in temp:
                continue
            temp.append(i)
            
        for i in range(97,123):
            if chr(i) in temp or chr(i)=='j':
                continue
            temp.append(chr(i))

        val = 0
        for i in range(n):
            for j in range(n):
                l[i][j] = temp[val]
                val+=1
        return l
    #--------------------------------------------------------------------------
    def diagram(string, flag):
        nonlocal details

        list_diagram = []
        if flag:
            if 'j' in string:
                string = string.replace('j', 'i')
            s = ''
            for i in range(len(string)):
                if i !=0:
                        if string[i-1] == string[i]:
                            s+='x'
                s+=string[i]
            print(s)
            details.append(s)
            new_s = ''
            val = 0
            while(val<=(len(s)-1)):
                if(val==(len(s)-1)):
                    try:
                        new_s += s[val]
                        break
                    except:
                        break
                if(s[val] == 'x'):
                    val+=1
                    continue
                new_s += s[val]+s[val+1]
                val+=2
            s = new_s
            if(len(s) % 2 != 0):
                s += 'x'
            for i in range(0, len(s), 2):
                list_diagram.append(s[i:i+2])
            print("Diagrams:::",list_diagram)
            details.append('Diagrams:::' + str(list_diagram))
            return list_diagram
        else:
            for i in range(0, len(string), 2):
                list_diagram.append(string[i:i+2])
            print("Diagrams:::",list_diagram)
            details.append('Diagrams:::' + str(list_diagram))
            return list_diagram
    #--------------------------------------------------------------------------
    def E():
        nonlocal details
        nonlocal output
        s = ''
        for i in dg:
            forAppend = ''
            print(i, end='->')
            forAppend += str(i) + '->'
            (x, y), (z, w) = (find_pos(i[0]),find_pos(i[1]))
            print(x,y,z,w)
            forAppend += str(x) + str(y) + str(z) +str(w) + ' & '
            if(y==w):
                x = (x+1)%5
                z = (z+1)%5
            if(x==z):
                y = (y+1)%5
                w = (w+1)%5
                w,y = y, w
            print(x,w,z,y, end='->')
            forAppend += str(x) + str(w) + str(z) + str(y) + ' -> '
            print( km[x][w]+km[z][y])
            forAppend += km[x][w]+km[z][y]
            s+= km[x][w]+km[z][y]
            print()
            details.append(forAppend)
        print("Encrypted text:::", s)
        output += s
    #--------------------------------------------------------------------------
    def D():
        nonlocal details
        nonlocal output
        nonlocal output2

        s = ''
        for i in dg:
            forAppend = ''
            print(i)
            forAppend += str(i) + '->'
            (x, y), (z, w) = (find_pos(i[0]),find_pos(i[1]))
            print(x,y,z,w)
            forAppend +=  str(x) + str(y) + str(z) + str(w)
            if(y==w):
                x = ((x-1)+5)%5
                z = ((z-1)+5)%5
            if(x==z):
                y = ((y-1)+5)%5
                w = ((w-1)+5)%5
                w,y = y, w
            print(x,w,z,y)
            forAppend +=  str(x) + str(w) + str(z) + str(y) + '->'
            print( km[x][w]+km[z][y])
            forAppend += km[x][w]+km[z][y]
            s+= km[x][w]+km[z][y]
            print()
            details.append(forAppend)
        print("Decrypted text:::", s)
        output += s
        #------------------------------
        new_s = ''
        if(s[len(s)-1]=='x'):
            l = len(s)-1
        else:
            l = len(s)
        for i in range(0, l):
            if s[i]=='x':
                if(s[i-1]==s[i+1] or (s[i]=='x' and i ==0)):
                    continue
            new_s += s[i]
        output2 += new_s + ' '
    #--------------------------------------------------------------------------
    def find_pos(char):
            for i in range(len(km)):
                if char in km[i]:
                    return (i, km[i].index(char))
    #--------------------------------------------------------------------------
    def print_km(km):
        nonlocal details
        print("Key matrix as follows: ")
        details.append("Key matrix as follows: ")
        for i in km:
            s = ''
            print(km.index(i), end = ' ')
            s += str(km.index(i)) + ' '
            for j in i:
                print(j, end = ' ')
                s += str(j) + ' '
            details.append(s)
            print()
    #--------------------------------------------------------------------------

    if(encryption == 'true'):
        for word in ip.split():
            t, k = word, key
            km = key_matrix(k)
            print_km(km)
            dg = diagram(t, 1)
            E()
            output += ' '
            output2 += ''
            details.append(' ')
    else:
        for word in ip.split():
            t, k = word, key
            km = key_matrix(k)
            print_km(km)
            dg = diagram(t, 0)
            D()
            output += ' '
            output2 += ''
            details.append(' ')
    result = {
        'details': details,
        'output': output,
        'output2': output2
    }

    return JsonResponse(result)