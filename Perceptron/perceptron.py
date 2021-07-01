# This is the perceptron function
# It takes five agruments and adjust the weight to learn from examples
# The five agruments are : threshold value,adjustment factor,initial weights, examples, and number of passes
# It does not return a value but it will print the process of learning as output
def perceptron(th_val,adj_val,weights,examples,pass_num):
    print("Starting weights: "+ str(weights))
    print("Threshold: "+str(th_val)+" Adjustment: "+str(adj_val))
    for x in range(pass_num):  
        print("\nPass "+str(x+1)+"\n")
        for i in range(len(examples)):
            example = examples[i][1]
            print("inputs: "+str(example))
            given_rc = examples[i][0]
            rc = find_result(th_val,weights,example)
            print("prediction: "+str(rc)+" answer: "+str(given_rc))
            if rc != given_rc:
                if rc == False:
                    for j in range(len(example)):
                        if example[j] == 1:
                            weights[j] += adj_val
                if rc == True:
                    for j in range(len(example)):
                        if example[j] == 1:
                            weights[j] -= adj_val
            print("adjusted weights: "+str(weights))
    return


# This is a help function to use giving exmaple and value to generate prediction result
# It takes three arguments: current threshold value, giving example, and current weights
# It will return a True or False as the result
def find_result(th_val,weights,example):
    my_val = 0
    for i in range(len(weights)):
        x = weights[i]*example[i]
        my_val = my_val + x
    if my_val > th_val:
        return True
    else:
        return False