<div align="center">
  <img src="readme-assets/banner.png" alt="HaninArchiver Banner" style="border-radius: 10px; width: 80%; height: 80%;">
</div>

<p align="center">
    <img src="https://img.shields.io/badge/language-C%2B%2B-blue" alt="Python">
    <img src="https://img.shields.io/github/license/farismuhammad17/HaninArchiver" alt="License">
</p>

> *"Memory is the diary that we all carry about with us."* — Oscar Wilde

*Hanin* (حنين) is the Arabic word for "Nostalgia". This project was built specifically for those giant folders with like 10 years of family photos (or something similar). Of course, these take a lot of space on the disk, and that's not useful, even if you are storing them on an external disk - no one uses these files often enough for them to take that much space.

## Why I made this

Personally, as the developer, I made this program because of a very small problem I had: I had two computers with photos and videos that were backed up from old phones. These computers ran on Windows, and eventually the operating system got too heavy for those computers' specs. As a result, I have another laptop that doesn't use Windows. But it felt like a waste to have two perfectly fine computers that I don't use simply because of Windows, so I wanted to move it to Linux.

Of course, the most important thing to do before one changes a system's operating system is to backup all the important data. In my case, that was many hundreds of gigabytes of family memories. These files were backups that were poorly done, and left many duplicates and files with old inefficient formats, and it was next to impossible to go through the thousands of files and figure out the duplicates myself.

I didn't bother with addressing that issue, and just moved everything to a newly bought 1 TB Hard Disk under two folders; "Laptop1" and "Laptop2". The total space that all of that occupied was almost 200 GB; but since I wasn't going to use the hard disk often, it didn't matter. Some time passed and I needed to use a hard disk with 1 TB of storage (for another project). Instead of buying another hard disk, I could just use the one I have.

The plan for me was simple: move the 200 GB of files into one of those old computers. The problem: this not only fills up the computer's disk space, it takes absolutely forever. Thus came this project - I have detailed its functioning in later sections.

## Usage

Make sure to run `make` to compile the C++ program.

Execute the [`__main__.py`](HaninArchiver/__main__.py) by `python path/to/HaninArchiver`. The following are the flags (you can also view them by running).

```
python HaninArchiver docs
```

> [!NOTE]  
> As of now, the program does not parse the arguments if there is a space in between. Avoid giving "My Folder", or any such input with a space for now.

* `-dir` **(required)**: Path to the folder you want to compress.
* `-save-to`: If omitted, the program will delete all unnecessary files, else, it will move all the unnecessary files to the directory you provide.
* `-zip`: Name of the `.7z` file (if you have compressing enabled).
* `--no-log`: Disables the automatic logging.
* `--no-rem-empty-files`: Disables automatic removal of files with 0 bytes of data.
* `--no-rem-dupes`: Disables deduplication.
* `--no-convert-img`: Disables image format conversion to `.webp`.
* `--no-convert-vid`: Disables video format conversion to `.mp4`.
* `--no-zip`: Disables zipping result into `.7z`.
* `--view-dupes`: Enables the program to create two videos of found duplicate images.

## Functionality

The following section is for the curious who wish to know the specific functioning of the program. Every feature listed here can be disabled through user flags.

### Preliminary processing

The program deletes all files that have 0 bytes, since they hold no value in the computation.

### Deduplication

To remove all duplicates is a $O(n^2)$ operation, because you are comparing every file to every other file. Of course, this program is being built for folders with thousands of files, so this step is done by filtering files one by one through different checks. The fastest, but less accurate, checks go first, and the slowest, but most accurate, checks go last.

#### Size grouping

If two files have different sizes, they can never be duplicates. This step creates a dictionary of lists that groups all files with the same file size.

> [!NOTE]  
> All hashing is done with xxHash (and can be changed easily in the source code if preferred).

#### Fast hashing

A hash map (using XXH64)is used to quickly check if duplicates exist, but unfortunately, files are big, and hashing the raw data takes time. Thus, this step hashes only the first 128 KB of data. If the first 128 KB of data is different, they are likely not duplicates.

#### Full hashing

This is the first step that genuinely takes a lot of time to complete, but fortunately, the previous steps have filtered out most of the non-duplicate files. This step hashes (using XXH128) the entire binary of a file and stores it. If two files have the same hash, it is most likely they are the same.

#### Byte-by-Byte checking

Hashing, though incredibly rare, may produce the same result for two separate sets of data. Because of all of the filtering we have done, it is *highly* unlikely that you have two files with the same hash that are not duplicates *(unless you are the kind of person to get struck by lightning thrice and happen to win the lottery seven times)*, but the chance is never $0$.

Since this is valuable data we are processing, checking each individual bit is paramount. Since this is a slow process, it is done through C++ for faster results. If two files' binary content is the exact same, they are definitely duplicates of each other, thus can finally be removed.

### Image conversions

Most of the data is going to be images, but older formats sometimes store a lot of unoptimised data. Fortunately, `.webp` is a good alternative, as it also preserves the picture's metadata. Thus we convert every picture into `.webp`.

### Video conversions

Similar to images, videos are also prevalent in the data we're going to be working with, so we convert everything into `.mp4`

> [!IMPORTANT]  
> If FFmpeg is not installed on your system, the program will skip over video conversions.

### Zipping

Among many compression algorithms, 7zip offers one that can be read directly from outside without needing you to extract it.

---

*Distributed under the MIT License. See [LICENSE](LICENSE) for more information.*
