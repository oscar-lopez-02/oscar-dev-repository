s = tf('s');
f0 = 25000;
w0 = 2 * pi * f0;

% Stage 1 Parameters
A_s1 = 2.0;
Q_s1 = 1.0;
b_s1 = 0.3617;

% Stage 2 Parameters
A_s2 = 2.75;
Q_s2 = 4.0;
b_s2 = 0.2373;

% Stage 3 Parameters
A_s3 = 2.5;
Q_s3 = 2.0;
b_s3 = 0.2373;

% Stage 4 Parameters
A_s4 = 2.5;
Q_s4 = 2.0;
b_s4 = 0.2373;

% Transfer Functions
H1 = ( (b_s1 * A_s1 * Q_s1 * w0) / Q_s1 * s ) / (s^2 + (w0/Q_s1)*s + w0^2);
H2 = ( (b_s2 * A_s2 * Q_s2 * w0) / Q_s2 * s ) / (s^2 + (w0/Q_s2)*s + w0^2);
H3 = ( (b_s3 * A_s3 * Q_s3 * w0) / Q_s3 * s ) / (s^2 + (w0/Q_s3)*s + w0^2);
H4 = ( (b_s4 * A_s4 * Q_s4 * w0) / Q_s4 * s ) / (s^2 + (w0/Q_s4)*s + w0^2);

% Total Cascaded Transfer Function
H_total = H1 * H2 * H3 * H4;
bode(H_total)
