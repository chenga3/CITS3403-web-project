#include <bits/stdc++.h>
using namespace std;

int main(int argc, char *argv[]) {

        int n;
        cin >> n;

        string s;
        cin >> s;

        for(int i = 0; i < n; i++) {
                if (s[i + 1] != s[i]) {
                        cout << s[i];
                }
        }

        return 0;

}
