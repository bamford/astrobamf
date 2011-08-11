<?php
function authors_process($authors, $surnames)
{
    $nmax = 5;
    $n = 0;
    $m = 0;
    $limited = array();
    $showname = array();
    foreach($authors as $a) {
        $ns = explode(',', $a);
        $surname = $ns[0];
        $showname = false;
        if ($surnames != null) {
            foreach ($surnames as $s) {
                if ($s == $surname) {
                  $surname = '<b>' . $s . '</b>';
                  $showname = true;
                  break;
                }
            }
        }
        if ($n < $nmax) {
            $limited[] = $surname;
            $m = $n;
        } else if ($showname) {
            if ($n + 1 != $m) {
                $limited[] = '...';
            }
            $limited[] = $surname;
            $m = $n;
        }
        $n = $n + 1;
    }
    if ($n + 1 != $m) {
        $limited[] = 'et al.';
    }
    return implode(', ', $limited);
}

//$ads_url = 'http://ukads.nottingham.ac.uk/';
$ads_url = 'http://adsabs.harvard.edu/';
$ads_url .= 'cgi-bin/nph-abs_connect?';
$ads_url .= 'db_key=AST&db_key=PRE&qform=AST&';
$ads_url .= 'start_nr=1&arxiv_sel=astro-ph&arxiv_sel=gr-qc&';
$ads_url .= 'start_mon=&start_year=&nr_to_return=100&start_nr=1&';
$ads_url .= 'jou_pick=ALL&article_sel=YES&ref_stems=&ALL&';
$ads_url .= 'sort=NDATE&data_type=SHORT_XML&author=';

$n = 'Bamford, Steven P';
$names = array(urlencode($n));
$surnames = array('Bamford');

$ads_url .= implode('%0D%0A', $names);

$ads_url_normal = str_replace('SHORT_XML', 'SHORT', $ads_url);
echo 'Automatically retrieved from <a href="' . $ads_url_normal . '">ADS</a>.'."\n";

//Using normal php method
//$xmlstr = file_get_contents($ads_url);
//Using Wordpress method:
$xmlstr = wp_remote_fopen($ads_url);

$xml = new SimpleXMLElement($xmlstr);

foreach ($xml->record as $record) {
  $authors = authors_process($record->author, $surnames);
  $pubdate = explode(' ', $record->pubdate);
  $year = $pubdate[1];
  $link = '';
  foreach ($record->link as $l) {
    if ($l['type'] == 'ABSTRACT') {
      $link = $l->url;
      break;
    }
  }
  echo "\n-----\n";
  echo '<b>[' . $record->title . '](' . $link . ")</b><br />\n";
  echo $authors, ", ", $year, ",<br />\n<em>", $record->journal, "</em>\n";
}
?>
