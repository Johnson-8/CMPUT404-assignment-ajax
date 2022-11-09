import json

def main():
    test_dict = {   
        'a': 'b',
        'f': 'g'    
        }

    print(type(test_dict))
    print(test_dict)

    # test_dict = '"""' + str(test_dict) + '"""'
    # print(test_dict)

    test_dict = json.dumps(test_dict)

    js_dict = json.loads(test_dict)
    print(type(js_dict))
    print(js_dict)

    return


main()