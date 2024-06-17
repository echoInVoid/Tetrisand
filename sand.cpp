#include <string>
using namespace std;

class Sand
{
    public:

    int type;
    int id; // 编号
    string color;

    Sand() = default;
    Sand(int t, string c, int n) : type(t), color(c), id{n} {}

    bool operator==(Sand a)
    {
        return this->type == a.type;
    }
};

extern "C"
{
    void init(int, int);
    int get(int, int);
    void set(int, int, int);
}

const Sand VOID = Sand(-1, "#000000", 0);
const Sand SAND_RED1 = Sand(0, "#B0482F", 1);
const Sand SAND_RED2 = Sand(0, "#8D3A26", 2);
const Sand SAND_YELLOW1 = Sand(1, "#DA9D2F", 3);
const Sand SAND_YELLOW2 = Sand(1, "#B98628", 4);
const Sand SAND_GREEN1 = Sand(2, "#5D8D28", 5);
const Sand SAND_GREEN2 = Sand(2, "#466B1F", 6);
const Sand SAND_BLUE1 = Sand(3, "#305995", 7);
const Sand SAND_BLUE2 = Sand(3, "#28497A", 8);
const Sand REMOVING = Sand(4, "#FFFFFF", 9); // 即将被删除

const Sand* S[] = {
    &VOID,
    &SAND_RED1,
    &SAND_RED2,
    &SAND_YELLOW1,
    &SAND_YELLOW2,
    &SAND_GREEN1,
    &SAND_GREEN2,
    &SAND_BLUE1,
    &SAND_BLUE2,
    &REMOVING
};

const Sand*** sands; // Actually Sand* sands[][]
int W, H;

void init(int listW, int listH)
{
    W = listW;
    H = listH;
    sands = new const Sand**[W];
    for (int i=0; i<W; i++)
        sands[i] = new const Sand*[H];

    for (int i=0; i<W; i++)
        for (int j=0; j<H; j++)
            sands[i][j] = &VOID;
}

bool validPos(int x, int y)
{
    return x>=0 && x<W && y>=0 && y<H;
}

int get(int x, int y)
{
    if (!validPos(x, y))
        return 0;
    return sands[x][y]->id;
}

void set(int x, int y, int s)
{
    if (validPos(x, y))
        sands[x][y] = S[s];
}