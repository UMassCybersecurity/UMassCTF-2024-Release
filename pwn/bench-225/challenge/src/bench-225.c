#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>

#define MAXIMUM_ADDITIONS 32

typedef struct {
    unsigned short CurrentWeight;
    unsigned short TargetWeight;
    unsigned short Max;
    unsigned short CurrentRep;
    unsigned short TargetRep;
    unsigned short Stamina;
} Barbell;

Barbell g_Barbell;

char *g_Quotes[] = {
    "I WILL NOT QUIT.",
    "It's in your mind!",
    "They don't know me son!",
    "Who's gonna carry the boats? And the logs?",
    "Don't stop when you're tired! Stop when you're done!",
};

__attribute__((constructor)) void init() {
    setbuf(stdin, 0LL);
    setbuf(stdout, 0LL);
    setbuf(stderr, 0LL);
}

void the_boats() {
    asm("pop %rax");
    asm("ret");
    asm("pop %rbx");
    asm("ret");
    asm("pop %rdi");
    asm("ret");
    asm("pop %rdx");
    asm("ret");
    asm("pop %rsi");
    asm("ret");
    asm("pop %rcx");
    asm("ret");
    asm("syscall");
    asm("ret");
    asm("mov %rax, %rdi");
    asm("ret");
}

int main() {
    int g_Choice = 0;

    printf(" __                                      __                ______    ______   _______  \n");        
    printf("/  |                                    /  |              /      \\  /      \\ /       | \n");      
    printf("$$ |____    ______   _______    _______ $$ |____         /$$$$$$  |/$$$$$$  |$$$$$$$/  \n");        
    printf("$$      \\  /      \\ /       \\  /       |$$      \\  ______$$____$$ |$$____$$ |$$ |____  \n");    
    printf("$$$$$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$$/ $$$$$$$  |/      |/    $$/  /    $$/ $$      \\ \n");       
    printf("$$ |  $$ |$$    $$ |$$ |  $$ |$$ |      $$ |  $$ |$$$$$$//$$$$$$/  /$$$$$$/  $$$$$$$  |\n");        
    printf("$$ |__$$ |$$$$$$$$/ $$ |  $$ |$$ \\_____ $$ |  $$ |       $$ |_____ $$ |_____ /  \\__$$ |\n");      
    printf("$$    $$/ $$       |$$ |  $$ |$$       |$$ |  $$ |       $$       |$$       |$$    $$/ \n");        
    printf("$$$$$$$/   $$$$$$$/ $$/   $$/  $$$$$$$/ $$/   $$/        $$$$$$$$/ $$$$$$$$/  $$$$$$/  \n");        
    printf("\n");

    printf("Grind doesn't stop.\n");
    printf("\n");

    g_Barbell.CurrentWeight = 0;
    g_Barbell.TargetWeight = 225;
    g_Barbell.Stamina = 140;
    g_Barbell.Max = 315;
    g_Barbell.TargetRep = 25;
    g_Barbell.CurrentRep = 0;

    while (1) {
        printf("====================================\n");
        printf("Name: Gary Goggins\n");
        printf("Goal: %d lbs x %d reps\n", g_Barbell.TargetWeight, g_Barbell.TargetRep);
        printf("Current Weight: %d\n", g_Barbell.CurrentWeight);
        printf("Rep: %d/%d\n", g_Barbell.CurrentRep, g_Barbell.TargetRep);
        printf("Stamina: %d\n", g_Barbell.Stamina);
        printf("====================================\n");
        printf("\n");

        printf("Choose an option:\n");
        printf("1. Add 10s\n");
        printf("2. Add 25s\n");
        printf("3. Add 45s\n");
        printf("4. Bench\n");
        printf("5. Remove Plate\n");

        if (g_Barbell.Stamina < 50 && g_Barbell.CurrentWeight >= g_Barbell.TargetWeight) {
            printf("6. Motivational Quote\n");
        }

        scanf("%d", &g_Choice);

        switch (g_Choice) {
            case 1:
                add_10s();
                break;
            case 2:
                add_25s();
                break;
            case 3:
                add_45s();
                break;
            case 4:
                if (g_Barbell.Stamina <= 0) {
                    printf("You are too tired to continue.\n");
                    break;
                } else {
                    bench();
                }
                break;
            case 5: {
                printf("\033[2J");
                printf("Weakness is a choice.\n");
                break;        
            }
            case 6: {
                if (g_Barbell.Stamina < 50 && g_Barbell.CurrentWeight >= g_Barbell.TargetWeight) {
                    motivation();
                }
                break;
            }
            default:
                printf("Invalid choice.\n");
                break;
        }
    }
}

unsigned short calculate_stamina_needed() {
    return g_Barbell.CurrentWeight / 14;
}

void printTextBox(const char *quote) {
    int width = strlen(quote) + 6;
    printf("|");
    for (int i = 0; i < width; i++) {
        printf("-");
    }
    printf("|\n");

    printf("|  \"%s\"  |\n", quote);

    printf("|");
    for (int i = 0; i < width; i++) {
        printf("-");
    }
    printf("|\n");
}

void add_10s() {
    printf("\033[2J");
    printf("Adding 10s\n");
    if (g_Barbell.CurrentWeight + 10 > g_Barbell.Max) {
        printf("On second thought... they don't allow that at this gym.\n");
        exit(0);
    }
    g_Barbell.CurrentWeight += 10;
    g_Barbell.CurrentRep = 0;
}

void add_25s() {
    printf("\033[2J");
    printf("Adding 25s\n");
    if (g_Barbell.CurrentWeight + 25 > g_Barbell.Max) {
        printf("On second thought... they don't allow that at this gym.\n");
        exit(0);
    }
    g_Barbell.CurrentWeight += 25;
    g_Barbell.CurrentRep = 0;
}

void add_45s() {
    printf("\033[2J");
    printf("Adding 45s\n");
    if (g_Barbell.CurrentWeight + 45 > g_Barbell.Max) {
        printf("On second thought... they don't allow that at this gym.\n");
        exit(0);
    }
    g_Barbell.CurrentWeight += 45;
    g_Barbell.CurrentRep = 0;
}

void motivation() {
    char quote[8];
    memset(quote, 0, sizeof(quote));
    printf("Enter your motivational quote: ");
    
    // Read quote.
    while (1) {
        int c = getchar();
        if (c == '\n' || c == EOF) {
            break;
        }
    }

    fgets(quote, 1000, stdin);

    // Print quote.
    printf("\033[2J");
    printf("Quote: \"");
    printf(quote);
    printf("\" - Gary Goggins");

    puts("...........................................................................:::::::::::::------------");
    puts("............................................................................::::::::::::------------");
    puts("............................................................................::::::::::::------------");
    puts("............................................................................:::::::::::-------------");
    puts(".....................................................=+++===.................::::::::::-------------");
    puts("..................................................++#**+++=====-............:::::::::::-------------");
    puts("................................................+####***+========-..........:::::::::::-------------");
    puts("...............................................+##%##**+====-======.........:::::::::::-------------");
    puts("..............................................+%##%%**++=-------===-.........::::::::::-------------");
    puts("..............................................##%%%%#*++===---=====+.........::::::::::-------------");
    puts("..............................................*%%%%%#***++=----====+........:::::::::::-------------");
    puts("..............................................+#%%%%#+=++===---===++........:::::::::::-------------");
    puts("..............................................+*#@@@@%#*+++*##*+=+=:-.......:::::::::::-------------");
    puts("............................................:%%*%%%#**%%#-=*#@@*=-=--#......:::::::::::-------------");
    puts("............................................-%##%%%%+-#%*---***=--====......:::::::::::-------------");
    puts(".............................................@%#%%#***%%*----==---==+:......:::::::::::-------------");
    puts(".............................................#%#%%####%%+--=-==--===-........::::::::::-------------");
    puts("..............................................=*%%%%%%%@#+%*-======:.........::::::::::-------------");
    puts("...............................................:#%%%%%%%#*+=--=====..........::::::::::-------------");
    puts("................................................%%%%%%%%%+++-======..........::::::::::-------------");
    puts("................................................#%%%%@%#+==-======+..........::::::::::-------------");
    puts(".................................................%%%%%%%%#*====++==:.........::::::::::-------------");
    puts(".................................................%@%%%%%**+====++==++*=-....:::::::::::-------------");
    puts("..............................................:#%%@@@%%@%%%#**+======*=+-=--::::::::::::------------");
    puts("..........................................:**%%%@%%@@%%%@%#+==++=====#++*+-==---::::::::------------");
    puts(".....................................-+**%%%%%%@@@@@@@%%%#*+=+++=====+++++==++++-==::::-------------");
    puts(".................................-+*#%#%%#%%%@%@@@@@@@%%%%#++++++++=++=====+++=+======--::---:------");
    puts("..............................:*#%#%%%%%@@@%%%@%@@@@@@%%%%%##*++++=*+*++=+=+==++=========-::--:-----");
    puts("............................-#%#%%%%%@@%%%%%%%%%%%%@%@%#%%%%#*++=*++++====**++**+====+=-=--::-:-----");
    puts("...........................*####%#%%%%%@%@%%%#*##*#*++#==*%%#++=***=*=++++#=#**+=+*====--=--:-------");
    puts("..........................=#####*#####%#%#@%%%%#*#***+*==+%##**+**=*#*+*+%=*##+#+*++======---:------");
    puts("..........................######%@*####*#%@%%*##*##***+*+*%%##***+*+#++=#+=%%*%**+*+=+===-:==:------");
    puts(".........................=%#@*%#*%**#**##%%%#**#**%#***#*#*#%#**+++**+*+%=#%*#***#++*=+-+==--:------");
    puts(".........................#%%##%*#%%++***#%@%+*#%**#%*=*+#**+###**=***++%#*%%+%@%**%*++*=+=----------");
    puts(".........................#%%*@*%+#@++**+#%%%*+#%*++%%*=+%*+***+*+++*+**%*#@*%%%%##*#***==+==::------");
    puts(".........................#%%%#@*%*%*+%++*%%#**##***##%#+++*###+*+****+##*%@+%@%@%%%#+**=====--------");
    puts(".........................%#@%@%%##@#+%#=*@%#**#%#+=###%#****#*+#*##+*=#%#@%=%@@@@@%%*#*++==---------");
    puts("........................+*%#%%%*@**@*%%=%%#**##%#=++##*%%*###***###***###@#+#@@@@@#%##*++===--------");
    puts("........................%%%@%+@%%%%@#@%+%%#*###%#**#%%####%##*####*++#%#%@*+*%@@@@%%%+==*+=-=-------");
    puts("........................%%@%%@@*#@%@%@%#%###*%%##**##%##*#%%*##*##***#%#@%**#%@@*#%%%**++==+-==-----");
}

void bench() {
    printf("\033[2J");

    if (g_Barbell.CurrentRep == g_Barbell.TargetRep) {
        printf("You already finished the set, but okay...\n");
    } 

    if (g_Barbell.CurrentWeight == 0) {
        printf("You need to add some weight first.\n");
        return;
    } else if (g_Barbell.CurrentWeight > g_Barbell.Max) {
        printTextBox("CENSORED");
        printf("The barbell bent once you picked it up. What a miracle. I think we're done here...\n");
        exit(0);
    }

    if (g_Barbell.Stamina <= 0) {
        printf("You are too tired to bench this.\n");
        return;
    }

    unsigned short stamina_needed = calculate_stamina_needed();
    if ((short)(g_Barbell.Stamina - stamina_needed) <= 0) {
        printf("Barely made that one...\n");
        g_Barbell.Stamina = 0;
    } else {
        g_Barbell.Stamina -= stamina_needed;
    }

    printf("Benching...\n");
    g_Barbell.CurrentRep++;

    if (g_Barbell.CurrentWeight >= g_Barbell.TargetWeight && g_Barbell.CurrentRep >= (g_Barbell.TargetRep / 2.0)) {
        printTextBox(g_Quotes[rand() % 4]);
    }
    printf("Stamina: %d\n", g_Barbell.Stamina);

    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⠶⣶⣄⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣷⣶⣤⡀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⡟⣠⣴⡬⣿⣇⣀⣀⣀⣀⣀⣠⢿⣿⣿⣿⣿⣿⣷⡀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣿⣧⠛⡯⣬⣿⡟⠒⠒⠒⠒⠒⢪⣾⣿⣷⣿⣿⣿⣷⠒⠛⠟\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡦⡯⠋⠀⠀⠀⠀⠀⠀⠘⠙⣿⣿⣿⣽⡿⠃⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⣸⠇⠀⠀⠀⠀⠀⠀⠀⢰⢢⢫⡌⠉⠉⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣌⣷⠀⠀⠀⠀⠀⠀⠀⢸⣹⢸⡇⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠈⣙⠢⠤⠤⢄⣀⠀⠀⢸⡼⢾⣱⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⣀⣀⣀⣀⡠⠤⠾⠃⠀⠞⠈⢀⢀⣩⢏⠙⢶⡎⠓⠹⢿⡹⣄⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⣤⡒⠒⢹⠉⠉⠉⠉⢀⡩⠭⡀⠉⠉⠀⠋⡵⣁⣄⣠⠀⠀⠀⠀⠀⠀⠂⠀⠘⢢⣽⠃⠰⣿⣶⣿⣿⡆⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⢸⡌⠀⠀⠈⡆⠀⠀⣰⠋⢀⠀⠸⠀⠀⠀⠀⢘⠨⢩⢳⣇⡀⡀⠀⠀⠀⠀⠈⠈⠈⠀⠀⠽⣹⣿⣿⣿⠃⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⢸⠀⠈⢺⣹⡞⣀⣼⣣⠀⠎⢤⠞⠀⠀⠀⠀⣸⠐⡇⠘⣼⣿⣿⣿⣿⣿⣶⡦⠤⠤⠤⣶⣿⣿⣭⡿⠿⠆⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠈⡇⠀⠈⣿⠉⠉⠉⢸⠃⢀⠈⣷⣶⣶⣶⣿⣥⣤⣴⣾⠿⠶⠾⠿⠿⠿⣿⣿⣟⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⣇⠀⠀⣧⠀⠀⠀⢸⠀⠆⠂⢸⣿⡇⠀⠉⣽⣿⣿⣦⣤⣀⠀⣠⠀⠀⠈⠻⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⢸⡀⠀⣿⠀⠀⠀⢸⠀⠀⠀⣿⣿⡇⢠⢺⣿⡿⠉⠛⠿⢿⣿⣿⣦⣄⣠⡆⠈⡻⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⠀⠈⡇⠀⡿⠀⠀⠀⠘⠀⠀⢠⣿⣿⣣⣳⣿⡟⠁⠀⠀⠀⠀⠈⠙⠛⠿⣿⣿⣾⣧⣙⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("⠀⠀⠀⢀⣜⣇⣰⣸⡀⠀⠀⠀⡄⠀⢸⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⢿⣿⣿⣿⣿⣧⣀⠀⠀⠀⠀⠀\n");
    printf("⣤⡐⡲⣿⣍⣯⣿⣷⣽⠀⢀⡎⣙⣦⣼⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⡿⢿⣿⣿⣟⣁⣀⠀⠀⠀\n");
    printf("⠉⠛⠛⠓⠛⠛⠤⠮⣕⠷⠮⢿⣟⢿⣅⣏⡛⣷⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠓⠒⠳⢽⣿⣿⣣⠀⠀\n");
    printf("⠀⠀⠀⠀⠀⠀⠀⠸⣶⣒⣤⣼⠽⠾⠽⠃⠈⠙⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n");
    printf("\n");
    

    if (g_Barbell.CurrentRep >= g_Barbell.TargetRep) {
        printf("You have completed the set!\n");
    }
}
