// simulation_science_combine.cc
// Program to determine various simulated statistics
// for use in combining the mxu/obs/science images.

// Steven Bamford
// Started 04-12-2002 13:36
// $Id: simulation_science_combine.cc,v 1.20 2002/12/11 16:40:22 spb Exp spb $

/* Determines bias for estimating:
   - true standard deviation of population from 
     MAD of lowest n values of a sample of m,
   - true mean and median of population from mean and
     median of lowest n values of a sample of m.
   And also determines the errors on these biases.
*/

// includes
#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <numeric>
#include <algorithm>
#include "NRgdev.h" // provides NRgdev() 

using namespace std;

// global constants
// simulation:
// NB: to preserve randomness n_sim * n < 10^8
const int n_sim = 1000000;   // no. of simulations
int n;             // no. in each sample (SET IN LOOP HEADER BELOW)
int n_low;         // no. of low pixels to use (SET IN LOOP BELOW)
// noise model:
const double ron = 3.0;      // readout noise (e-)
                             // rough average of both chips
const double gain = 1.43;    // gain (ADU/e-)
                             // from image headers
int bg_level = 1000;  // background level (ADU)
                      // ~ strong galaxy continuum = 1000
int f_level;       // feature level (ADU) (SET IN LOOP HEADER BELOW)
                   // ~ med-strong sky line = 4000
double f_level_sd; // feature stdev of variation (SET IN LOOP HEADER BELOW)
                   // ~ for med-strong sky lines = 0.15 * f_level
// paths
const char* pix_path = "sim_pixels";
const char* log_path = "sim_results";

//define results output destination
ofstream log_file;
ostream& rout = log_file;
//define progress output destination
ostream& pout = cout;

// function declarations:
// statistics
double median(vector<double> vec);
double mean(vector<double> vec);
double stdev(vector<double> vec);
double mad(vector<double> vec);
// make pixels from model
void make_pixels(vector<double>& pixels);
// do simulation of sampling
vector< vector<double> > sim(vector<double>& pixels);
// write out details
void write_pixels(vector<double> pixels);
void write_results(vector< vector<double> > stats);
void write_params();

// main function:
int main()
{
  // runs simulation and organises output
  // set up log file
  log_file.open(log_path);
  //debug// pout << "Starting" << endl;
  // loop over desired values of n, n_low and bg/feature variation
  for (n = 4; n >=2; n -= 2)
    {
      pout << "n: " << n << endl;
      n_low = n - 1;
      for (f_level = 0; f_level <= 10000; f_level += 2000)
	{
	  pout << "f_level: " << f_level << endl;
	  for (int f_level_sd_pc = 5; f_level_sd_pc <= 25; f_level_sd_pc += 10)
	    {
	      pout << "f_level_sd_pc: " << f_level_sd_pc << endl;
	      f_level_sd = f_level_sd_pc * f_level / 100.0;
	      vector<double> pix;
	      vector< vector<double> > stats;
	      //debug// pout << "Making pixels" << endl;
	      make_pixels(pix);
	      //debug// pout << "Writing pixels" << endl;
	      //write_pixels(pix);
	      //debug// pout << "Beginning simulation" << endl;
	      stats = sim(pix);
	      //debug// pout << "Writing results" << endl;
	      write_params();
	      write_results(stats);
	    }
	}
    }
  // close log file
  log_file.close();
}


// function definitions:

// functions for calculating statistics
double median(vector<double> vec) //vec MUST be sorted
{
  //debug// pout << "Calculating median... ";
  if (vec.size() == 0) pout << "Warning vec.size() == 0" << endl;
  int med_index = int(vec.size() / 2);
  double med;
  if (vec.size() % 2 != 0)
    { // odd
      med = vec.at(med_index);
    }
  else
    { // even
      med = 0.5 * (vec.at(med_index) + vec.at(med_index - 1));
    }
  return med;
}

double mean(vector<double> vec)
{
  //debug// pout << "Calc. mean... ";
  if (vec.size() == 0) pout << "Warning vec.size() == 0" << endl;
  double sum = accumulate(vec.begin(), vec.end(), 0.0);
  //debug// pout << "sum = " << sum << "   ";
  //debug// pout << "mean = " << sum / vec.size() << "\n"; 
  return (sum / vec.size());
}

double stdev(vector<double> vec)
{ // adapted from NR function moment
  //debug// pout << "Calc. stdev... ";
  int j;
  double ave, var, sdev;
  double ep=0.0, s, sum;
  int size = vec.size();
  s = sum = accumulate(vec.begin(), vec.end(), 0.0);
  ave = s / size; 
  var = 0.0;
  for (j=0; j<size; j++) 
    { 
      s = vec.at(j) - ave;
      ep += s; 
      var += (s*s); 
    } 
  var = (var - ep*ep/size) / (size-1);
  sdev = std::sqrt(var);
  //debug// pout << "sum = "  << sum  << "   ";
  //debug// pout << "size = " << size << "   ";
  //debug// pout << "ave = "  << ave  << "   ";
  //debug// pout << "sdev = " << sdev << "\n";
  return sdev;
}

double mad(vector<double> vec) // mean absolute deviation
{ // adapted from NR function moment
  //debug// pout << "Calculating mad... ";
  int j;
  double ave, adev, s; 
  int size = vec.size();
  s = accumulate(vec.begin(), vec.end(), 0.0);
  ave = s / size; 
  adev = 0.0; 
  for (j=0; j<size; j++) 
    { 
      adev += fabs(vec.at(j) - ave); 
    } 
  adev /= size; 
  return adev;
}

double range(vector<double> vec)
{
  //debug// pout << "Calculating range... ";
  double max = *max_element(vec.begin(), vec.end());
  double min = *min_element(vec.begin(), vec.end());
  double range = max - min;
  return range;
}

vector< vector<double> > sim(vector<double>& pixels)
{
  // carries out the simulation and returns a vector
  // containing the bias for the sd, mean and median,
  // and their respective errors.
  // vectors to store the accumulated statistics in
  vector<double> median_vec;
  vector<double> mean_vec;
  vector<double> stdev_vec;
  vector<double> mad_vec;
  vector<double> range_vec;
  vector<double> median_low_vec;
  vector<double> mean_low_vec;
  vector<double> stdev_low_vec;
  vector<double> mad_low_vec;
  vector<double> range_low_vec;

  pout << "Looping " << n_sim << " times:" 
       << endl << "% complete: ";

  for (int i = 0; i < (n_sim * n); i += n)
    { // loop n_sim times
      if (i % (n * n_sim/(10)) == 0)
	{
	  pout << (i * 100 / (n * n_sim)) << " . ";
	  pout.flush();
	}
      vector<double> sample(n);  // to store current sample
      // fill sample
      for (int j = 0; j < n; j++)
	{ 
	  sample.at(j) = pixels.at(i+j); 
	  //debug// pout << "sample[" << j << "] = ";
	  //debug// pout << sample.at(j) << endl;
	}
      // sort the sample
      sort(sample.begin(), sample.end());
      vector<double> sample_low(n_low);  // to store low sample
      // fill sample_low
      for (int j = 0; j < n_low; j++)
	{ 
	  sample_low.at(j) = sample.at(j); 
	  //debug// pout << "sample_low[" << j << "] = ";
	  //debug// pout << sample_low.at(j) << endl;
	}
      // calculate sample statistics
      double sample_median = median(sample);
      double sample_mean   = mean(sample);
      double sample_stdev  = stdev(sample);
      double sample_mad    = mad(sample);
      double sample_range  = range(sample);
      double sample_low_median = median(sample_low);
      double sample_low_mean   = mean(sample_low);
      double sample_low_stdev  = stdev(sample_low);
      double sample_low_mad    = mad(sample_low);
      double sample_low_range  = range(sample_low);
      // put into cumulative vectors
      median_vec.push_back(sample_median);
      mean_vec.push_back(sample_mean);
      stdev_vec.push_back(sample_stdev);
      mad_vec.push_back(sample_mad);
      range_vec.push_back(sample_range);
      median_low_vec.push_back(sample_low_median);
      mean_low_vec.push_back(sample_low_mean);
      stdev_low_vec.push_back(sample_low_stdev);
      mad_low_vec.push_back(sample_low_mad);
      range_low_vec.push_back(sample_low_range);

    }
  pout << endl;

  // calculate overall statistics
  //debug// pout << "Calculating overall statistics..." << endl;
  // following vectors contain value [0], error [1], and maybe sd [2].
  const int val = 0, err = 1, sd = 2;
  const double inv_sqrt_n_sim = 1.0 / std::sqrt(double(n_sim));
  const double inv_true_mean  = 1.0 / (bg_level + f_level);
  const double true_stdev = stdev(pixels);
  const double inv_true_stdev = 1.0 / true_stdev;
  //debug// cout << "True stdev = " << true_stdev << endl;
  // for normal samples
  //debug// pout << "for normal samples" << endl;
  double all_median     = mean(median_vec);
  double all_median_err = stdev(median_vec) * inv_sqrt_n_sim;
  double all_mean       = mean(mean_vec);
  double all_mean_err   = stdev(mean_vec) * inv_sqrt_n_sim;
  double all_stdev      = mean(stdev_vec);
  double all_stdev_err  = stdev(stdev_vec) * inv_sqrt_n_sim;
  double all_mad        = mean(mad_vec);
  double all_mad_err    = stdev(mad_vec) * inv_sqrt_n_sim;
  double all_range      = mean(range_vec);
  double all_range_err  = stdev(range_vec) * inv_sqrt_n_sim;
  // for low samples
  //debug// pout << "for low samples" << endl;
  double low_median       = mean(median_low_vec);
  double low_median_stdev = stdev(median_low_vec);
  double low_median_err   = low_median_stdev * inv_sqrt_n_sim;
  double low_mean         = mean(mean_low_vec);
  double low_mean_stdev   = stdev(mean_low_vec);
  double low_mean_err     = low_mean_stdev * inv_sqrt_n_sim;
  double low_stdev        = mean(stdev_low_vec);
  double low_stdev_stdev  = stdev(stdev_low_vec);
  double low_stdev_err    = low_stdev_stdev * inv_sqrt_n_sim;
  double low_mad          = mean(mad_low_vec);
  double low_mad_stdev    = stdev(mad_low_vec);
  double low_mad_err      = low_mad_stdev * inv_sqrt_n_sim;
  double low_range        = mean(range_low_vec);
  double low_range_stdev  = stdev(range_low_vec);
  double low_range_err    = low_range_stdev * inv_sqrt_n_sim;
  // calculate biases
  //debug// pout << "Calculating biases" << endl;
  vector<double> bias_all_median(2);
  bias_all_median.at(val) = all_median * inv_true_mean;
  bias_all_median.at(err) = all_median_err * inv_true_mean;
  vector<double> bias_all_mean(2);
  bias_all_mean.at(val) = all_mean * inv_true_mean;
  bias_all_mean.at(err) = all_mean_err * inv_true_mean;
  vector<double> bias_all_stdev(2);
  bias_all_stdev.at(val) = all_stdev * inv_true_stdev;
  bias_all_stdev.at(err) = all_stdev_err * inv_true_stdev;
  vector<double> bias_all_mad(2);
  bias_all_mad.at(val) = all_mad * inv_true_stdev;
  bias_all_mad.at(err) = all_mad_err * inv_true_stdev;
  vector<double> bias_all_range(2);
  bias_all_range.at(val) = all_range * inv_true_stdev;
  bias_all_range.at(err) = all_range_err * inv_true_stdev;
  vector<double> bias_low_median(3);
  bias_low_median.at(val) = low_median * inv_true_mean;
  bias_low_median.at(err) = low_median_err * inv_true_mean;
  bias_low_median.at(sd)  = low_median_stdev * inv_true_mean;
  vector<double> bias_low_mean(3);
  bias_low_mean.at(val) = low_mean * inv_true_mean;
  bias_low_mean.at(err) = low_mean_err * inv_true_mean;
  bias_low_mean.at(sd)  = low_mean_stdev * inv_true_mean;
  vector<double> bias_low_stdev(3);
  bias_low_stdev.at(val) = low_stdev * inv_true_stdev;
  bias_low_stdev.at(err) = low_stdev_err * inv_true_stdev;
  bias_low_stdev.at(sd)  = low_stdev_stdev * inv_true_stdev;
  vector<double> bias_low_mad(3);
  bias_low_mad.at(val) = low_mad * inv_true_stdev;
  bias_low_mad.at(err) = low_mad_err * inv_true_stdev;
  bias_low_mad.at(sd)  = low_mad_stdev * inv_true_stdev;
  vector<double> bias_low_range(3);
  bias_low_range.at(val) = low_range * inv_true_stdev;
  bias_low_range.at(err) = low_range_err * inv_true_stdev;
  bias_low_range.at(sd)  = low_range_stdev * inv_true_stdev;
  // now fill vector to return
  vector< vector<double> > results;
  results.push_back(bias_all_median);
  results.push_back(bias_all_mean);
  results.push_back(bias_all_stdev);
  results.push_back(bias_all_mad);
  results.push_back(bias_all_range);
  results.push_back(bias_low_median);
  results.push_back(bias_low_mean);
  results.push_back(bias_low_stdev);
  results.push_back(bias_low_mad);
  results.push_back(bias_low_range);
  return results;
}

void make_pixels(vector<double>& pixels)
{
  // fill vector pixels with pixel values based on noise model
  // clear the pixels vector
  pixels.clear();
  long* seed = new long(123);  // for NRgdev()
  const int n_pix = n_sim * n; // number of pixels to generate
  pout << "Making " << n_pix << " pixels" << endl
       << "% complete: ";
  double inv_gain = 1 / gain;  // to avoid division in loop
  for (int i = 0; i < n_pix; i++)
    {
      if (i % (n_pix/10) == 0)
	{
	  pout << (i * 100 / n_pix) << " . ";
	  pout.flush();
	}
      double value = bg_level; // pixel value (ADU)
      double f_value = f_level + NRgdev(seed) * f_level_sd;
      value = value + f_value;
      if (value < 0.0)
	{
	  value = 0.0;
	}
      else
	{
	  double ccd_noise = std::sqrt(value * inv_gain + ron*ron) * gain;
	  value = value + NRgdev(seed) * ccd_noise;
	  if (value < 0.0) value = 0.0;
	}
      value = int(value);
      pixels.push_back(value);
    }
  pout << endl;
  delete seed;
}

void write_pixels(vector<double> pixels)
{
  // write out pixel values to a file for examination
  pout << endl << "Writing pixel values to file " 
       << pix_path << endl << endl;
  rout << endl << "Writing pixel values to file " 
       << pix_path << endl << endl;
  ofstream pixfile;
  pixfile.open(pix_path);
  vector<double>::iterator pix_it;
  for (pix_it = pixels.begin(); pix_it != pixels.end(); pix_it++)
    {
      pixfile << *pix_it << endl;
    }
  pixfile.close();
}

void write_results(vector< vector<double> > stats)
{
  // write out parameters and results of the simulation
  // to a log file

  // stats vectors contain value [0], error [1], and maybe sd [2].
  const int val = 0, err = 1, sd = 2;
  
  // set formatting of output
  rout.precision(5);
  rout.setf(ios::fixed, ios::floatfield);

  rout << endl;
  rout << "Results for " << n_sim << " samples:" << endl << endl;

  rout << "For normal samples of " << n << " : " << endl;
  rout << "Bias on median   = "  << stats.at(0).at(val)
       << " +- " << stats.at(0).at(err) << endl;
  rout << "Bias on mean     = "  << stats.at(1).at(val)
       << " +- " << stats.at(1).at(err) << endl;
  rout << "Bias on std. dev. = "  << stats.at(2).at(val)
       << " +- " << stats.at(2).at(err) << endl;
  rout << "Bias on MAD      = "  << stats.at(3).at(val)
       << " +- " << stats.at(3).at(err) << endl;
  rout << "Bias on range    = "  << stats.at(4).at(val)
       << " +- " << stats.at(4).at(err) << endl;

  rout << endl << "For samples of lowest " << n_low 
       << " out of " << n << " : " << endl;
  rout << "Bias on median    = "  << stats.at(5).at(val)
       << " +- " << stats.at(5).at(err) 
       << "  (SD = " << stats.at(5).at(sd) 
       << " = " << 100 * stats.at(5).at(sd) / stats.at(5).at(val)
       << "%)" << endl;
  rout << "Bias on mean      = "  << stats.at(6).at(val)
       << " +- " << stats.at(6).at(err)
       << "  (SD = " << stats.at(6).at(sd) 
       << " = " << 100 * stats.at(6).at(sd) / stats.at(6).at(val)
       << "%)" << endl;
  rout << "Bias on std. dev. = "  << stats.at(7).at(val)
       << " +- " << stats.at(7).at(err)
       << "  (SD = " << stats.at(7).at(sd) 
       << " = " << 100 * stats.at(7).at(sd) / stats.at(7).at(val)
       << "%)" << endl;
  rout << "Bias on MAD       = "  << stats.at(8).at(val)
       << " +- " << stats.at(8).at(err)
       << "  (SD = " << stats.at(8).at(sd) 
       << " = " << 100 * stats.at(8).at(sd) / stats.at(8).at(val)
       << "%)" << endl;
  rout << "Bias on range     = "  << stats.at(9).at(val)
       << " +- " << stats.at(9).at(err)
       << "  (SD = " << stats.at(9).at(sd) 
       << " = " << 100 * stats.at(9).at(sd) / stats.at(9).at(val)
       << "%)" << endl;
  rout << endl;
}

void write_params()
{
  // prints out global parameters
  rout << endl << "--- Simulation parameters ---" << endl
       << "Number of simulations:   " << n_sim << endl
       << "Number in each sample:   " << n     << endl
       << "Number in 'low' samples: " << n_low << endl;
  rout << endl << "--- CCD parameters ---" << endl
       << "Read out noise (e-): " << ron << endl
       << "Gain (ADU/e-): " << gain << endl;
  rout << endl << "--- Flux levels (ADU per pixel) ---" << endl
       << "Background level (constant): " << bg_level << endl
       << "Feature level (varying):     " << f_level << endl
       << "Feature level std. dev.:     " << f_level_sd << endl
       << endl;
}
