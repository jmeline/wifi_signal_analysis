use URI::Escape;

#### Define Color codes ###
$color_theta90 = "FF8000";
$color_phi0    = "00FF00";
$color_phi90   = "0000FF";

$root = "../";
opendir(DIR, $root) || die("file not found");
@Export_files = sort(grep(/Export/, readdir(DIR)));
closedir(DIR);

sub percent_above_threshold {
	my($pname, $cut) = @_;
	my @arr_signal;

	$extract_frequency = "2440000000";
	$signalcount = 0;
	$count = 0;
	$threshold = -5;
	$totalsignal = 120;
	$plot_data = "";
	$plot_data2 = "";
	$waterfall = "";
	print ("\n\npname: $pname\n\n cut: $cut\n\n");
	# everything is in lines2
	# print ("Lines2: ", join(", ", @lines2));
	foreach(@lines2) {
		@parts = split;
		# print ("[63] Parts: ", length(@parts), "\n\n");
		if ($parts[0] == $extract_frequency) {
			$count++;
			
			if ($parts[2] >= $threshold) { 
				$signalcount++; 
			} 
			push @arr_signal, $parts[2];
			if ($cut eq 'Theta90') {
				$plot_data = sprintf("%.2f", ($parts[2] + 15.0) * 5.0 ).",".$plot_data;
			} else {
				if ($count <= 60) {
					$plot_data = sprintf("%.2f", ($parts[2] + 15.0) * 5.0 ).",".$plot_data;
				} else {
					$plot_data2 = sprintf("%.2f", ($parts[2] + 15.0) * 5.0 ).",".$plot_data2;
				}
			}
		}
	}

	# print("plot_data: $plot_data\n\n");
	# print("plot_data2: $plot_data2\n\n");

	if ($cut ne 'Theta90') { 
		$plot_data = $plot_data.$plot_data2; 
	}

	chop $plot_data; #remove trailing ,
	my @sorted_signals = sort { $b <=> $a } @arr_signal;

	$results = 100* int ( 10000 *$signalcount /$totalsignal)/10000;
	#$results = substr $signalcount,0,6; 
	print("-> ",$results," % of signals above ",$threshold," dbi ");

	#store hash of hash of products->cut|percent above -5dBi
	$tests->{$pname}{$cut}{"percentAbove"} = $results/100;

	#store hash of hash of products->cut|chart data string
	$tests->{$pname}{$cut}{"plot_data"} = $plot_data;  

	#build waterfall chart string
	foreach(-30...10) {
		my $counter = 0;
		while ($sorted_signals[$counter++] >= $_) {
			last if ($counter >= @sorted_signals);
		}
		$waterfall .= sprintf("%.2f,", $counter/121.0*83.333);
	}

	chop $waterfall;
	$tests->{$pname}{$cut}{"waterfall"} = $waterfall;

	if ($results <= 30 ) { 
		print "FAIL \n";
	} else {
		print " \n";  
	}

	$signalcount = 0;
}                                                              

## Start of the program ##
foreach(@Export_files)
{

	print("$_\n") unless -d;

	$INPUT_FILE = $_;
	$INPUT_FILE_ALL = "../".$INPUT_FILE ;


	#$root_name ="../Export21JAN09";
	$root_name = $INPUT_FILE_ALL;

	$folder_name = $root_name."/.";
	$folder_name2 = $root_name."/";


	opendir(DIR,$folder_name  ) || die("file not found");
	@effic_files = sort(grep(/efficien/, readdir(DIR)));
	closedir(DIR);

	opendir(DIR,$folder_name  ) || die("file not found"); 
	@phi0_files = sort(grep(/phi=0/, readdir(DIR)));
	closedir(DIR);

	opendir(DIR,$folder_name ) || die("file not found");
	@phi90_files = sort(grep(/phi=90/, readdir(DIR)));
	closedir(DIR);

	opendir(DIR,$folder_name) || die("file not found");
	@theta90_files = sort(grep(/theta=90/, readdir(DIR)));
	closedir(DIR);

	my %tests;

	############## Signal Coverage Measurements ###########

	######### CUT THETA=90 ################

	foreach(@theta90_files) {


		$INPUT_FILE = $_;
		print($folder_name2.$INPUT_FILE," ");
		$INPUT_FILE_ALL = $folder_name2.$INPUT_FILE ;

		$product_name = $INPUT_FILE_ALL;
		$product_name =~ s/-theta=90.txt//;
		$product_name =~ s/..\/Export//;

		open(FILEE,$INPUT_FILE_ALL) || die("file not found"); 
		@lines2 = <FILEE>;
		close (FILEE);


		# percent_above_threshold($product_name, "Theta90"); 
	}

	######### CUT PHI=0 ################

	foreach(@phi0_files) {


		$INPUT_FILE = $_;

		print($folder_name2.$INPUT_FILE," ");
		#print($INPUT_FILE,"\t");
		$INPUT_FILE_ALL = $folder_name2.$INPUT_FILE ;

		$product_name = $INPUT_FILE_ALL;
		$product_name =~ s/-phi=0.txt//;
		$product_name =~ s/..\/Export//;

		open(FILEE,$INPUT_FILE_ALL ) || die("file not found"); 
		@lines2 = <FILEE>;
		close (FILEE);


		# percent_above_threshold($product_name, "Phi0"); 
	}


	######### CUT PHI=90 ################

	foreach(@phi90_files) {
		$INPUT_FILE = $_;
		print($folder_name2.$INPUT_FILE," ");
		#print($INPUT_FILE," ");
		$INPUT_FILE_ALL = $folder_name2.$INPUT_FILE ;

		$product_name = $INPUT_FILE_ALL;
		$product_name =~ s/-phi=90.txt//;
		$product_name =~ s/..\/Export//;

		open(FILEE,$INPUT_FILE_ALL) || die("file not found"); 
		@lines2 = <FILEE>;
		close (FILEE);


		# percent_above_threshold($product_name, "Phi90"); 
	}



	############ EFFICIENCY ##################

	foreach(@effic_files) {
		print("$_\n") unless -d;

		$INPUT_FILE = $_;
		$INPUT_FILE_ALL = $folder_name2.$INPUT_FILE ;

		open(FILEE,$INPUT_FILE_ALL) || die("file not found"); 
		@lines = <FILEE>;
		close (FILEE);

		$aveeff = 0;

		$product_name = $INPUT_FILE_ALL;
		$product_name =~ s/-efficiency.txt//;
		$product_name =~ s/..\/Export//;


		foreach(@lines) {
			print "\n" if m/^1/;
			print $_ if m/^Fr/;
			@value = split if m/^2/;
			$freq = substr $value[0],0,4;
			$effic = substr $value[1],0,6;

			#store hash of hash of products->freq|efficiency
			$tests->{$product_name}{$freq} = $effic;


			print $freq,"\t",$effic,"\n" if m/^2/;
			$aveeff = $effic if $freq=="2440";
		}


		print "\n",$INPUT_FILE_ALL,"-> 2440 Mhz=",$aveeff;
		if ($aveeff <= .30) { 
			print " FAIL\n\n";
			} 
		else {
			print "\n\n"; 
		}

		$aveeff = 0;
	}
}


 ############### Collect information from user ###########
 foreach (sort keys %$tests) {
 	push @test_arr, $_;
 	print @test_arr.". $_ \n";
 }

 print "Enter tests to compare using test numbers seperated by spaces: ";
 $compare_list = <STDIN>;

 print "Output file: ";
 $out_file = <STDIN>;

 open HTML_REPORT, "> $out_file" or die "cannot open file for writing!\n";

 ################# HTML Output +###############

 select HTML_REPORT;

 @compare = split /\s+/, $compare_list;

 $k1 = $test_arr[$compare[0] - 1];

 ################# Efficiency  +###############

 print "<!-- Efficiency Table\n";

 #print header row
 print "\t";
 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[1]."\t";
 }
 print "\n\t";
 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[0]."\t";
 }
 print "\n";

 #print table
 foreach ( sort keys %{$tests->{$k1}} ) {
 	next if (($_ eq "") or ($_ eq "Theta90") or ($_ eq "Phi0") or ($_ eq "Phi90"));
 	print "\"$_\"\t";
 	$freq = $_;
 	foreach (@compare) {
 		print $tests->{$test_arr[$_ - 1]}{$freq}."\t";
 	}
 	print "\n";
 }

 print "-->\n";


 #generate google chart URL
 print "<img src=\"";
 print "http://chart.apis.google.com/chart?chs=1000x300&cht=bvg&chxt=x,y,x&chds=0,1.0&chco=7b7dff,9C0000,63cf00,00007b,ffff00,334455&chbh=a&chg=0,10&chm=h,FF0000,0,0.3,1&chf=c,s,EFEFEF&chtt=Efficiency&chdl=2.402%20GHz|2.420%20GHz|2.440%20GHz|2.460%20GHz|2.483%20GHz|2.500%20GHz&chxl=0:|";

 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[1]."|";
 } 

 print "1:|0.0|0.1|0.2|0.3|0.4|0.5|0.6|0.7|0.8|0.9|1.0|2:|";

 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[0]."|";
 } 

 print "&chd=t:";

 foreach ( sort keys %{$tests->{$k1}} ) {
 	next if (($_ eq "") or ($_ eq "Theta90") or ($_ eq "Phi0") or ($_ eq "Phi90"));
 	$freq = $_;
 	foreach (@compare) {
 		print $tests->{$test_arr[$_ - 1]}{$freq};
 		print "," unless ($_ eq $compare[@compare - 1]);
 	}
 	print "|" unless ($freq eq "2500");
 }

 print "\">\n\n";

 ################# Omnidirectional Cuts +###############

 print "<!-- Omnidirectional Table\n";

 #print header row
 print "\t";
 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[1]."\t";
 }
 print "\n\t";
 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[0]."\t";
 }
 print "\n";

 #print table
 print "Theta90\t";
 foreach (@compare) {
 	print $tests->{$test_arr[$_ - 1]}{"Theta90"}{"percentAbove"};

 	print "\t" unless ($_ eq $compare[@compare - 1]);
 }
 print "\nPhi0\t";
 foreach (@compare) {
 	print $tests->{$test_arr[$_ - 1]}{"Phi0"}{"percentAbove"};
 	print "\t" unless ($_ eq $compare[@compare - 1]);
 }
 print "\nPhi90\t";
 foreach (@compare) {

 	print $tests->{$test_arr[$_ - 1]}{"Phi90"}{"percentAbove"};
 	print "\t" unless ($_ eq $compare[@compare - 1]);
 }

 print "\n-->\n";

 #generate google chart URL
 print "<img src=\"";
 print "http://chart.apis.google.com/chart?chs=1000x300&cht=bvg&chxt=x,y,x&chds=0,1.0&chco=$color_theta90,$color_phi0,$color_phi90&chbh=a&chg=0,10&chm=h,FF0000,0,0.3,1&chf=c,s,EFEFEF&chtt=Percentage of signals above -5 dBi&chdl=Theta90|Phi0|Phi90&chxl=0:|";

 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[1]."|";
 } 

 print "1:|0.0|0.1|0.2|0.3|0.4|0.5|0.6|0.7|0.8|0.9|1.0|2:|";

 foreach (@compare) {
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print $titles[0]."|";
 } 

 print "&chd=t:";

 foreach (@compare) {
 	print $tests->{$test_arr[$_ - 1]}{"Theta90"}{"percentAbove"};

 	print "," unless ($_ eq $compare[@compare - 1]);
 }
 print "|";
 foreach (@compare) {
 	print $tests->{$test_arr[$_ - 1]}{"Phi0"}{"percentAbove"};
 	print "," unless ($_ eq $compare[@compare - 1]);
 }
 print "|";
 foreach (@compare) {

 	print $tests->{$test_arr[$_ - 1]}{"Phi90"}{"percentAbove"};
 	print "," unless ($_ eq $compare[@compare - 1]);
 }

 print "\">\n\n";

 ################# do the 2D cut plots +###############
 foreach (@compare) { 
 	@titles = split(/\//, $test_arr[$_ - 1]);
 	print "<p>";
 	#Theta90
 	print "<img src=\"";
 	print "http://chart.apis.google.com/chart?cht=r&chs=547x547&chtt=";
 	print uri_escape($titles[1]." (".$titles[0].") Theta = 90 Cut");
 	print "&chd=t:";
 	print $tests->{$test_arr[$_ - 1]}{"Theta90"}{"plot_data"};
 	print "&chco=$color_theta90&chls=2.0,4.0,0.0&chxt=y,x&chxl=0:|-15dB|-10dB|-5dB|0dB|5dB&chxr=1,360,3,3&chxs=1,000000,7|0,0000FF&chm=h,FF0000,0,0.5,0.5,-1|V,000000,0,0,0.1|V,000000,0,15,0.1|V,000000,0,30,0.1|V,000000,0,45,0.1|V,000000,0,60,0.1|V,000000,0,75,0.1|V,000000,0,90,0.1|V,000000,0,105,0.1";
 	print "\">\n\n";
 	#Phi0
 	print "<img src=\"";
 	print "http://chart.apis.google.com/chart?cht=r&chs=547x547&chtt=";
 	print uri_escape($titles[1]." (".$titles[0].") Phi = 0 Cut");
 	print "&chd=t:";
 	print $tests->{$test_arr[$_ - 1]}{"Phi0"}{"plot_data"};
 	print "&chco=$color_phi0&chls=2.0,4.0,0.0&chxt=y,x&chxl=0:|-15dB|-10dB|-5dB|0dB|5dB&chxr=1,360,3,3&chxs=1,000000,7|0,0000FF&chm=h,FF0000,0,0.5,0.5,-1|V,000000,0,0,0.1|V,000000,0,15,0.1|V,000000,0,30,0.1|V,000000,0,45,0.1|V,000000,0,60,0.1|V,000000,0,75,0.1|V,000000,0,90,0.1|V,000000,0,105,0.1";
 	print "\">\n\n";	
 	#Phi90
 	print "<img src=\"";
 	print "http://chart.apis.google.com/chart?cht=r&chs=547x547&chtt=";
 	print uri_escape($titles[1]." (".$titles[0].") Phi = 90 Cut");
 	print "&chd=t:";
 	print $tests->{$test_arr[$_ - 1]}{"Phi90"}{"plot_data"};
 	print "&chco=$color_phi90&chls=2.0,4.0,0.0&chxt=y,x&chxl=0:|-15dB|-10dB|-5dB|0dB|5dB&chxr=1,360,3,3&chxs=1,000000,7|0,0000FF&chm=h,FF0000,0,0.5,0.5,-1|V,000000,0,0,0.1|V,000000,0,15,0.1|V,000000,0,30,0.1|V,000000,0,45,0.1|V,000000,0,60,0.1|V,000000,0,75,0.1|V,000000,0,90,0.1|V,000000,0,105,0.1";
 	print "\">\n\n";

 	#composite waterfall chart
 	print "<p>";
 	print "<img src=\"";
 	print "http://chart.apis.google.com/chart?chtt=";
 	print uri_escape($titles[1]." (".$titles[0].") Composite Waterfall Chart");
 	print "&chdl=Theta90|Phi0|Phi90&chxl=3:|%20|Probability|%20|2:|%20|Signal%20Strength%20(dBi)|%20&chs=600x500&cht=lc&chxt=x,y,x,y&chxr=0,-30,10,2|1,0,1.2,0.1&chg=0,8.333&chf=c,s,EFEFEF&chm=V,FF0000,0,25,1.0&chco=$color_theta90,$color_phi0,$color_phi90&chd=t:";
 	print $tests->{$test_arr[$_ - 1]}{"Theta90"}{"waterfall"}."|";
 	print $tests->{$test_arr[$_ - 1]}{"Phi0"}{"waterfall"}."|";
 	print $tests->{$test_arr[$_ - 1]}{"Phi90"}{"waterfall"}."\">\n\n";	
 }


 close HTML_REPORT;

 select STDOUT;

