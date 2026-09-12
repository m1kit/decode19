#include <png.h>

#include <array>
#include <cstdint>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

using Pixel = std::array<std::uint8_t, 3>;
using PixelGrid = std::vector<std::vector<Pixel>>;

/** Decode a row-major 2-D pixel array and return text without a newline. */
std::string decode(const std::string& codeType, const PixelGrid& pixels) {
    throw std::runtime_error("decoder not implemented for " + codeType);
}

PixelGrid loadPixels(const char* path) {
    png_image image{};
    image.version = PNG_IMAGE_VERSION;
    if (!png_image_begin_read_from_file(&image, path))
        throw std::runtime_error("cannot read PNG");
    image.format = PNG_FORMAT_RGB;
    std::vector<std::uint8_t> bytes(PNG_IMAGE_SIZE(image));
    if (!png_image_finish_read(&image, nullptr, bytes.data(), 0, nullptr))
        throw std::runtime_error("cannot decode PNG");

    PixelGrid pixels(image.height, std::vector<Pixel>(image.width));
    for (std::size_t y = 0; y < image.height; ++y)
        for (std::size_t x = 0; x < image.width; ++x) {
            const std::size_t offset = 3 * (y * image.width + x);
            pixels[y][x] = {bytes[offset], bytes[offset + 1], bytes[offset + 2]};
        }
    return pixels;
}

int main(int argc, char** argv) {
    static const std::unordered_set<std::string> supported = {
        "japanese_braille", "morse", "code39", "pzn", "ean13", "telepen",
        "dx_film_edge", "hccb", "aztec_rune", "code128",
        "data_matrix", "qr", "micro_qr", "rmqr", "aztec", "pdf417",
        "micro_pdf417", "databar_expanded_stacked", "maxicode"
    };
    if (argc != 3) {
        std::cerr << "usage: decoder CODE_TYPE IMAGE_PATH\n";
        return 2;
    }
    if (!supported.contains(argv[1])) {
        std::cerr << "unsupported code type: " << argv[1] << '\n';
        return 2;
    }
    try {
        std::cout << decode(argv[1], loadPixels(argv[2])) << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
