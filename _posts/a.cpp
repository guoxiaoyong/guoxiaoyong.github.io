#include <map>

double div(int m, int n) {

    return (double)m / (double)n;
}

int div(int m, int n) {

    return m/n;
}

std::pair<int, int> div(int m, int n) {

    return std::make_pair(m/n, m%n);
}

