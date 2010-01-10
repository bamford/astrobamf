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

$ukads_url = 'http://ukads.nottingham.ac.uk/';
$ukads_url .= 'cgi-bin/nph-abs_connect?';
$ukads_url .= 'db_key=AST&db_key=PRE&qform=AST&';
$ukads_url .= 'start_nr=1&arxiv_sel=astro-ph&arxiv_sel=gr-qc&';
$ukads_url .= 'start_mon=&start_year=&nr_to_return=100&start_nr=1&';
$ukads_url .= 'jou_pick=ALL&article_sel=YES&ref_stems=&ALL&';
$ukads_url .= 'sort=NDATE&data_type=SHORT_XML&author=';

$n = 'Bamford, Steven P';
$names = array(urlencode($n));
$surnames = array('Bamford');

$ukads_url .= implode('%0D%0A', $names);

$ukads_url_normal = str_replace('SHORT_XML', 'SHORT', $ukads_url);

$xmlstr = wp_remote_fopen($ukads_url);
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
