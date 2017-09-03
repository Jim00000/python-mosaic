#include <utility>
#include <map>
#include <vector>

namespace cpp {
    class Voronoi {
    public:
        void diagram(
            int,
            int,
            std::vector<int>,
            std::vector<int>,
            std::map<int,std::vector<std::pair<int,int>>>*
        );
    };
}