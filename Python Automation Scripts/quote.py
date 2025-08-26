import random,colorama



class quote():
    def __init__(self):
        self.landing_page()

    def landing_page(self):
        colorama.init()
        print(colorama.Fore.GREEN+"  WELCOME TO MOTIVATIONAL QUOTE  ".center(100,"|"))
        print(colorama.Fore.RESET)
        print(colorama.Fore.CYAN+"1.Success\n2.Inspiring\n3.Dance\n4.Breakup\n5.Emotional\n6.Alone\n7.Cristiano Ronaldo\n8.Beautiful\n9.Art\n10.Amazing\n11.Angry\n12.Attitude\n13.Hope\n14.Powerful\n15.Respect\n16.Simplicity\n17.Funny\n18.Birthday\n19.Friends\n20.Food")
        print(colorama.Fore.MAGENTA+"CHOOSE ANY OPTION FROM 1-20")
        print(colorama.Fore.RESET)
        option = int(input(colorama.Fore.YELLOW+"Option:".strip()))
        print(colorama.Fore.RESET)
       
        if option == 1:
            self.success()
        elif option ==2:
            self.inspiring()
        elif option ==3:
            self.dance()
        elif option ==4:
            self.breakup()
        elif option ==5:
            self.emotional()
        elif option ==6:
            self.alone()
        elif option ==7:
            self.ronaldo()
        elif option ==8:
            self.beautiful()
        elif option ==9:
            self.art()
        elif option ==10:
            self.amazing()
        elif option ==11:
            self.angry()
        elif option ==12:
            self.attitude()
        elif option ==13:
            self.hope()
        elif option ==14:
            self.powerful()
        elif option ==15:
            self.respect()
        elif option ==16:
            self.simplicity()
        elif option ==17:
            self.funny()
        elif option ==18:
            self.birthday()
        elif option ==19:
            self.friend()
        elif option ==20:
            self.food()
        else:
            print(colorama.Fore.RED+"Please input number from 1-20\nPlease try again")
            print(colorama.Fore.RESET)
            
    def success(self):
        print(colorama.Fore.GREEN+"SUCCCESS QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Failure is success in progress","Shallow men believe in luck.Strong men believe in cause and effect","The successful warrior is the average man,with laser-like focus","Success is never accidental","90% of your plans are going to fail no matter what you do.Get used to it.","The difference between successful people and very successful people say 'no' to almost everything.","One can have no smaller or greater mastery than mastery of oneself."]
        charse = random.choice(word)
        print(charse)
    
    def inspiring(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["My life is my message.","Not how long,but how much well you have lived is the main thing.","I love those who can smile in trouble...","Life is what happens when you're bussy making other plans.","It is better to be hated for what you are than to be loved for what you are not.","Do not take life too seriously.You will never get out of it alive."]
        charse = random.choice(word)
        
        print(charse)     

    def dance(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["There are shortcuts to happiness,and dancing is one of them.","Work like you don't need the money.Love like you've never been hurt.Dance like nobody,s watching.","We're fools whether we dance or not,so we might as well dance","Let us reaad and let us dance - two amusements that will never do any harm to the world.","Those move easiest who have learn'd to dance","Poetry is to prose as dancing is to walking","Opportunity dances with those already on dancing floor.","Dancing is the poetry of foot.","Dance is the hidden language of the soul."]
        charse = random.choice(word)
        
        print(charse)    
    
    def breakup(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["My rear-view mirror had officially fallen off,no more looking back!","Nothing lasts forever","Life is to taste,not to waste","Like some wines, our love could neither mature nor travel","Love is blind,be careful","One day you will cry for me like I cied for you.","Some mistakes are committed one time","Is changing my relationship status to 'Out of order","Strong people stand up for themselves,but stronger people stand up for others","Crazy people will always do weird stuff.","I know only that I know nothing.","The most painful memory I have is of when I walked away and you let me leave.","Sometimes I just wonder if it is worth all of this...","Just give me time and I will get over you.","I didn't want to be the one to forget","It's hard to tell your mind to stop loving someone when your heart still does.","I would rather die of love than let love die.","Dear Insomnia...I think we really need to break up... I don't love you anymore...","When you are through changing,you are through.","I hope you're doing fine all alone.","I wish you weren't in my dreams.","I just hope that you miss me a little when I'm gone.","Is tired of crying,yeah,I'm smiling,but inside I'm dying...!!","Love is a beautiful mistake of my life.","I'LL never leave you - BIGGEST LIE.","Since I'm always second in your life,it's time I make you last in mine","Before you let go.Remember the reason why you were hanging on.","It's too late to take back all that you put me through...I'm moving on with my life.","You broke a promise and made me realize.It was all just a lie.","Love is My Favourite Mistake","Pain is inevitable.Suffering is optional.","Never even know if you never try.","When this is over,remember,I didn't WALK Away,You pushed Me Away..","Dear Bad Luck...Let's break up","Sometimes You need to stand alone to find out who you really are..","Wonders if this will ever get easier...","Just because I let you go,doesn't mean I wanted to"]
        charse = random.choice(word)
        
        print(charse)    

    def emotional(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["You think I've changed.Truth is you never really knew the real me.","I wonder if I've met the person I'm going to marry.","You never understand it unti you experience it.","Why are you trying so hard to fit in when you were born to stand out?","It doesn't matter what you do.It matters who you do it with.","Knowledge is like underwear.It is useful to have it, but not neccesary to shaow it off."]
        charse = random.choice(word)
        
        print(charse)    

    def alone(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["When the people you love are gone,you're alone.","I don't want to be alone,I want to be left alone.","Alone we can do so little;together we can do so much.","Justice cannot be for one side alone,but must be for both.","Remember,man does not live on bread alone:Sometimes he needs a little buttering up.","Marriage is good for those who are afraid to sleep alone at night."]
        charse = random.choice(word)
        
        print(charse)    
 

    def  ronaldo(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["My father always taught me that when you help other people, then God will give you double. And that's what has really happened to me. When I have helped other people who are in need, God has helped me more.","There are people out there who hate me and who say I'm arrogant, vain, and whatever. That's all part of my success. I am made to be the best.","Winning - that's the most important to me. It's as simple as that.","I don't mind people hating me, because it pushes me.","Talent without working hard is nothing.","Many people look at me and think they know me but they don't at all. This is the real me. I am a humble person, a feeling person. A person who cares about others, who wants to help others.","I'm living a dream I never want to wake up from."," “Scoring goals is a great feeling, but the most important thing to me is that the team is successful - it doesn’t matter who scores the goals as long as we’re winning.”",". “I think sometimes the best training is to rest.”"," “I feel endless need to learn, to improve, to evolve, not only to please the coach and the fans, but also to feel satisfied with myself.”"," “I’m not going to change the world. You’re not going to change the world. But we can help - we can all help.”","“It is my conviction that there are no limits to learning, and that it can never stop, no matter what our age.”","“If you don’t believe you are the best, then you will never achieve all that you are capable of.”"," “Dreams are not what you see in your sleep; they are the things that don’t let you sleep.”","“There is no harm in dreaming of becoming the world’s best player. It is all about trying to be the best. I will keep working hard to achieve it but it is within my capabilities.”","“Your love makes me strong. Your hate makes me unstoppable.”"," “Maybe they hate me because I’m too good!”"," “The most important thing is the family. Keep your family healthy, good, and take care of your family, because this is the most important thing in the world.”"]
        charse = random.choice(word)
        
        print(charse)    
    def beautiful(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["He who sacrifices his beard for a woman deserves neither.", " Think of all the beauty still left around you and be happy"]
        charse = random.choice(word)
        
        print(charse)    

    def art(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Art is either revolution or plagiarism","The cheif enemy of creativity is  'good' sense"]
        charse = random.choice(word)
        
        print(charse)    
   

    def amazing(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Silence is the sleep that nourishes wisdom", "I decided it is better to scream.Silence is the real crime against humanity"]
        charse = random.choice(word)
        
        print(charse)    

    def angry(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Sometimes hearing the music is just the best way to ignore the world", "Anger blows out the lamp of the mind"]
        charse = random.choice(word)
        
        print(charse)    

    def attitude(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Every problem comes with some solution..If it doesn't have any solution, it's a Girl","I'm not lazy, I'm  a master of energy conservation."]
        charse = random.choice(word)
        
        print(charse)    

    def hope(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Every cloud has a silver lining", "While ther's life, there's hope"]
        charse = random.choice(word)
        
        print(charse)    

    def powerful(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Freedom lies in being bold","To enjoy freedom we have to control ourselves","Freedom, in any case is only possible by constantly struggling for it."]
        charse = random.choice(word)
        
        print(charse)    

    def respect(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Respecting someone indicate the quality of your personality","Respect for the truth comes close to being the basis for all morality"]
        charse = random.choice(word)
        
        print(charse)    

    def simplicity(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["This less I needed, the better I felt","Let silence take you to the core of life"]
        charse = random.choice(word)
        
        print(charse)    

    def funny(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["This suspense is terrible I hope it wiill last","Go to Heaven for climate, Hell for the company."]
        charse = random.choice(word)
        
        print(charse)    

    def birthday(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["You are the sunshine in my life each second of every hour.Happy birthday to my love","May this day bring countless happinesss and endless joy and live with peace.Happy Birthday"]
        charse = random.choice(word)
        
        print(charse)    

    def friend(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["Just wanted to say thank you for coming into my life and being my TRUE FRIEND.","A true friend reaches and touches your heart"]
        charse = random.choice(word)
        
        print(charse)
   
    def food(self):
        print(colorama.Fore.GREEN+"INSPIRING QUOTE".center(50,"."))
        print(colorama.Fore.RESET)
        word =["I enjoy long romantic walks to the fridge","Chips have little nutritional value.That's why you need to eat the whole bag."]
        charse = random.choice(word)
        
        print(charse)                                                                                                    
wev = quote()        