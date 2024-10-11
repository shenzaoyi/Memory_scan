main.exe : main.cpp scan.cpp
	g++ -m64 main.cpp scan.cpp -o main

hello.exe : hello.cpp
	g++ -Wno-pointer-arith -m64 hello.cpp -o hello.exe

run: main.exe hello.exe
	./hello.exe | ./main.exe

clean:
	rm -f *.o *.exe