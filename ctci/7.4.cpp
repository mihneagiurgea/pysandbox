#include <stdio.h>

int negative(int a) {
    if (a > 0)

}

int multiply(int a, int b) {
    int sol = 0;

    if (b > 0) {
        for (int i = 0; i < b; i++)
            sol += a;
    } else {
        for (int i = b; i < 0; i++)
            sol += a;
    }
    return sol;
}

int division(int a, int b) {
    int sol = 0;
    int ahead = abs(b);
    for (; ahead < abs(a); ahead += abs(b), sol += abs(b));
    return sol;
}

int main() {
    printf("Hello, world!\n");
    printf("%d\n", multiply(3, 7));
    printf("%d\n", multiply(3, -7));
    printf("%d\n", multiply(-3, 7));
    printf("%d\n", multiply(-3, -7));

    return 0;
}