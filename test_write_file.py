from functions import write_file as wf

wf.write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
wf.write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
wf.write_file("calculator", "/tmp/temp.txt", "this should not be allowed")