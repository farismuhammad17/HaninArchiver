#include <fstream>
#include <vector>
#include <cstring>

extern "C" {
    int check_if_identical(const char* path1, const char* path2) {
        std::ifstream file1(path1, std::ios::binary);
        std::ifstream file2(path2, std::ios::binary);

        if (!file1 || !file2) return -1;

        const size_t buffer_size = 65536;
        std::vector<char> buffer1(buffer_size);
        std::vector<char> buffer2(buffer_size);

        while (file1.good() && file2.good()) {
            file1.read(buffer1.data(), buffer_size);
            file2.read(buffer2.data(), buffer_size);

            if (file1.gcount() != file2.gcount()) return 0;
            if (std::memcmp(buffer1.data(), buffer2.data(), file1.gcount()) != 0) return 0;
        }

        return 1;
    }
}
