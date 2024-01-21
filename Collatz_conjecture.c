#include <stdio.h>
#include <stdlib.h>
#define m 50

struct node{
    int data;
    struct node *next;
};

struct hash{
    struct node *head;  //pointing to list of nodes or list of elements in same index
    int count;  //no. of elements in the same index (causing collision)
}HashTable[m];

void initialise()
{
    int i;
    for(i=0;i<m;i++)
    HashTable[i].head=NULL;

}

void insert_chaining(int val)
{

   struct node *temp=(struct node *)malloc(sizeof(struct node));
    temp->data=val;
    temp->next=NULL;

    if(HashTable[val%m].head==NULL)
    {
        HashTable[val%m].head = temp;
        HashTable[val%m].count = 1;
    }
    else
    {
        temp->next = HashTable[val%m].head; //inserting newest value as head of the slot
        HashTable[val%m].head = temp;
        HashTable[val%m].count++;   //no. of elements in the same index hence incremented

    }


}

int search(int val)
{
    struct node *ptr=HashTable[val%m].head;
    if(ptr!=NULL && ptr->data==val)
    {
        return 1;
    }
   
        while(ptr!=NULL)
        {
            if(ptr->data==val)
            {
                return 1;
            }
            ptr=ptr->next;
        }
    return 0;

}

void print_hashtable()
{
    int i;
    printf("Index  Count       Data\n");
    for(i=0;i<m;i++)
    {
        

        if (HashTable[i].head!=NULL)
        {
            printf("  ");
            printf("%d  |   ", i);
            printf ("%d   |   ", HashTable[i].count);
            struct node *ptr = HashTable[i].head;
            while(ptr!=NULL)
            {
                if(ptr->next==NULL)
                {
                    printf("%d", ptr->data);
                    break;
                }
                else
                {
                    printf("%d --> ", ptr->data);
                    ptr=ptr->next;
                }

            }
        printf("\n");
        }
        

    }

}

int main()
{
    long int i;
    long int x;
    

    for(x=1;x>0;x++)
    {
        initialise();   //in each iteration, HT acts as storage for all the elements in the sequence
        i=x;
        while(i!=1 && !search(i))   //current elm in sequence isn't already there in hash table, cuz if it is already there, we have a loop.. and conjecture is false
        {
            insert_chaining(i); //inserting each elm. in sequence to a hash table

            if(i%2==0)
            i=i/2;
            else
            i=3*i+1;

            
        }
        //after loop, either 1 is reached, or current elm in seq. is already there in HT (i.e loop is found) conjecture proved for current number x
        if(i==1)
        {
            printf("Collatz conjecture true for %ld.\n",x);
            continue;
        }
        else if (search(i))
        {
            printf("\n%ld in the 3n+1 sequence for %ld appears twice, forming a loop that isn't 421, hence does not result in 1. So collatz conjecture is proven to be false.\n",i,x);
            break;
        }
        
        
    }
}
