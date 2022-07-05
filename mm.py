import random

def taking_random_output_total_vote(input)  :
    d=(str(input).split("*")[-1].replace("Random","").replace("random","").replace("(","").replace(")","").replace(".","").replace(" - ",",").replace("%","")).split(",")
    x=d[0]
    y=d[-1]
    output=f'{random.randint(int(x),int(y))}'
    return int(output)
Total_vote=taking_random_output_total_vote("Random(300 - 1200)")
print(Total_vote)
total_likes_dislikes=int(Total_vote)*int(taking_random_output_total_vote("Total vote * Random(.40,.60)"))/100
Likes_count=total_likes_dislikes*int(taking_random_output_total_vote("total likes + dislikes * random(.55,.75)"))/100
Dislikes_count=total_likes_dislikes-Likes_count



