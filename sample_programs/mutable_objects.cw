
.a = [1, 2, 3];
.b = .a;
append .a 4;
print .a;
print .b;
.b = copy .b;
append .a 5;
print .a;
print .b;

.A = new {.a = 1; .b = 2;};
.B = .A;
.A.c = 3;
print .A;
print .B;
.B = copy .B;
.A.d = 4;
print .A;
print .B;