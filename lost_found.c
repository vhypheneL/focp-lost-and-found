#include <stdio.h>
#include <string.h>        
#include <ctype.h>     // Including this Library to use tolower() function 

typedef struct Item {            // Grouping 5 variables with different Data Types
    int id;
    char status[10];     // "LOST" or "FOUND"
    char itemName[50];
    char location[50];
    char contact[30];
} Item;

void toLowerStr(char dest[],char src[]){   // Converting a string to all lowers
    int i=0;
    while (src[i]!='\0') {
        dest[i]=tolower(src[i]);
        i++;
    }
    dest[i]='\0';
}

void addunderscores(char str[]){     // Replacing spaces with underscores in Item name
    int i=0;
    while (str[i] != '\0'){
        if (str[i] ==' ') str[i] = '_' ;
        i++;
    }
}

void removeunderscores(char str[]){    // Replacing underscores with spaces for Display
    int i=0;
    while (str[i] != '\0'){
        if (str[i]=='_') str[i] = ' ';
        i++;
    }
}

int loadItems(struct Item items[]){    // Reading all the saved items from items.txt into an array
    FILE* fp=fopen("items.txt","r");
    if (fp==NULL) return 0; // FILE doesnt exist yet (i.e. no items added)
    int count =0;
    while (count < 100 && fscanf(fp, "%d %s %s %s %s",
                                    &items[count].id,
                                    items[count].status,
                                    items[count].itemName,
                                    items[count].location,
                                    items[count].contact) == 5){          // To ensure fscan is not taking the EOF terminator 
        count ++;

    }
    fclose(fp);
    return count;
}

void addItem(char status[],char name[], char loc[], char contact[]){       // Adding a new lost/found item to items.txt
    Item items[100];
    int count = loadItems(items);
    int newId =1;
    if (count>0) newId = items[count-1].id + 1;   // Auto-increment ID
    addunderscores(name);
    addunderscores(loc);
    addunderscores(contact);
    
    FILE* fp=fopen("items.txt","a");  // "a" = opening the file in append mode
    if (fp==NULL){
        printf("Error opening database file.\n");
        return;
    }
    fprintf(fp, "%d %s %s %s %s\n",newId,status,name,loc,contact);
    fclose(fp);
    printf("SUCCESS: Item #%d recorded.\n",newId);
}

void searchorListItems(char keyword[]){      // Searching and Listing the items
    Item items[100];
    int count = loadItems(items);
    char lowerKey[50];
    toLowerStr(lowerKey, keyword);

    int foundcount=0;
    for (int i=0;i<count;i++){
        char nameCopy[50], locCopy[50], contactCopy[30];
        strcpy(nameCopy, items[i].itemName);
        strcpy(locCopy, items[i].location);
        strcpy(contactCopy, items[i].contact);

        removeunderscores(nameCopy);
        removeunderscores(locCopy);
        removeunderscores(contactCopy);

        char lowerName[50], lowerLoc[50];
        toLowerStr(lowerName,nameCopy);
        toLowerStr(lowerLoc,locCopy);

        if (strlen(lowerKey) == 0 || strstr(lowerName,lowerKey) != NULL || strstr(lowerLoc,lowerKey) != NULL) {
            printf("%d |%s |%s |%s |%s\n",items[i].id,items[i].status,nameCopy,locCopy,contactCopy);
            foundcount++;
        }
    }

    if (foundcount == 0) printf("EMPTY\n");
}

// Entry Point: Now we will receive command from the terminal or web server
int main(int argc, char* argv[]){
    if (argc < 2){
        printf("Usage: ./lost_found [add|list|search]\n");
        return 1;
    }

    if (strcmp(argv[1],"add") == 0 && argc == 6){
        addItem(argv[2],argv[3],argv[4],argv[5]);
    }
    else if (strcmp(argv[1],"list") == 0){
        searchorListItems("");
    }
    else if (strcmp(argv[1],"search") == 0 && argc == 3){
        searchorListItems(argv[2]);
    }
    else {
        printf("Invalid arguments.\n");
    }

    return 0;
}