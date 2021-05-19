# Scheduling_Column_Generation

In this problem, a staff roster will be created for a call center. A day schedule for call-center extends from 8:00AM through 8:00PM. We divide this into 48 15-minute periods since an estimate is made for the number of incoming calls per minute for every 15 minutes. The number of required operators can be determined per 15 minutes with the Erlang-C queue model. The following rules apply when creating a shift for an operator:

• A day shift cannot exceed 9 hours, but is not allowed to be shorter than 4 hours.
• If a shift exceeds 8 hours, 0.75 break time is required of which 0.5 hour contiguous. 
• If a shift exceeds 5.5 hours, a single break of 0.5 hours or two breaks of 0.25 hours is required. 
• For shorter shifts (less than 5.5 hours) a single break of 0.25 hours applies.
• Maximum contiguous time an operator can work without a break is 3.25 hours.

The problem is to generate a schedule where the total working time is minimal and the service level is met in every fifteen minutes.

Answering a phone call takes an average of 1/5 minute. An 80-20 service level is required, which means that 80% of the callers must get someone on the line within 20 seconds.  The estimated number of employees required differs per 15 minutes, therefore shift lengths, start and break times must differ, so that good solutions can be obtained that reach the service level.

The problem is to generate a schedule where the total working time is minimal and the service level is met in every fifteen minutes.

Problem data: 

The number of required operators per 15 minutes
d=[2,5,6,5,7,7,4,6,7,7,7,7,6,5,6,6,5,4,7,6,6,4,5,5,6,6,5,7,7,6,9,6,7,6,6,7,7,4,5,5,4,5,3,4,5,3,5,4]

Formulation:

Master Problem:

min  sum_s c_s * x_s
s.t. sum_s a_ts * x_s >= d_t  for all t=1:48
     x_s >= 0 , Integer for sin S
     
x_s is number of operators working shift s 
a_ts = 1 if in shift s, operator has to work in period t and 0 otherwise
S is the set of all shifts

reduced cost: sigma_s = cs − pi * A_s =  cs − sum_t pi_t * a_ts

if we make a new variable w_t = 1 if operator is working in shift t and 0 otherwise, then the subproblem is 

min  c_s - sum_t pi_t * w_t
s.t. w is a pattern

Note that cs = sum_t w_t and hence, c_s - sum_t pi_t * w_t = sum_t w_t - sum_t pi_t * w_t = sum_t w_t * (1-pi_t)

So the subproblem is 

min  sum_t w_t * (1-pi_t)
s.t. w is a pattern

Constraints for w being a pattern:

a minimum of 4 and a maximum of 9 hours of work in a shift.
16 <= sum_(t=1:48) w_t  <=36 

p_t = 1 if you have pause at time t, 0 otherwise
y_t = 1 if you are present at time t (work or break), 0 otherwise

w_t + p_t = y_t, for t = 1:48, (work + pause = present)

y_t can only change from 0 to 1 or twice from a 1 to a 0, namely when the working day starts and on
the moment the working day ends. Therefore, |y_t - y_(t−1)| can be 1 twice otherwise must be 0. So 

sum_(t=2:48) |y_t - y_(t−1)| <= 2

A 0 always changes to a 1, unless work is started at the very beginning of the day, then w_1 = 1. And 1 always changes to a 0, unless w_48 = 1. So 

sum_(t=2:48) |y_t - y_(t−1)| + w_1 + w_48 = 2

To ensure that the working day does not start, or is ended with a break, the following restriction is necessary:

p_1 = p_48 = 0

Everyone has 1 or 2 breaks per day, so there are a minimum of 2 and a maximum of 4
transitions from no pause to pause or vice versa:

2 <= sum_(t=2:48) |p_t - p_(t−1)| <= 4

num of working periods    num of 15 min break 
        23-26                   3   
        22-31                   2
        16-21                   1

So, number of 15-min breaks is determined by: floor(number of working periods / 10.55)

sum_(t=1:48) p_t < (sum_(t=1:48) w_t)/10.55
sum_(t=1:48) p_t > (sum_(t=1:48) w_t)/10.55 - 1

you always work max 3.25 hours back to back

sum_(j=t:t+13) w_j < 14

So the subproblem is

min  sum_t w_t * (1-pi_t)
s.t. 16 <= sum_(t=1:48) w_t  <=36 
     w_t + p_t = y_t, for t = 1:48, (work + pause = present)
     sum_(t=2:48) |y_t - y_(t−1)| + w_1 + w_48 = 2
     p_1 = p_48 = 0
     2 <= sum_(t=2:48) |p_t - p_(t−1)| <= 4
     sum_(t=1:48) p_t < (sum_(t=1:48) w_t)/10.55
     sum_(t=1:48) p_t > (sum_(t=1:48) w_t)/10.55 - 1
     sum_(j=t:t+13) w_j < 14 for t=1:48-13
     w_t, y_t, p_t binary for t=1:48
     
(absolute value constraints can be linearized easily)    

References:
[1] Annemieke van Dongen, Personeelsplanning en Kolomgeneratie, Vrije Universiteit Amsterdam, November 2005.
