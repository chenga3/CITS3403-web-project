#include <bits/stdc++.h>
using namespace std;

#define ULL unsigned long long

int main(void) {

    ULL n;
    cin >> n;

    unordered_set<ULL> s;

    for (ULL  i = 0; i < (ULL)sqrt(n) + 1; i++) {
        s.insert(i*i);
    }

    for (ULL i = 0; i < (ULL)sqrt(n) + 1; i++) {
        if (s.find(n - i*i) != s.end()) {
            cout << i << " " << (ULL)sqrt(n - i*i) << "\n";
            return 0;
        }
    }

    cout << "-1" << "\n";

    return 0;
}
