use strict;
use vars qw($VERSION %IRSSI);

use Irssi;
$VERSION = '1.00';
%IRSSI = (
    authors     => 'siesta',
    contact     => 'thecoconutnutisagiantnut@gmail.com',
    name        => 'alert',
    description => 'alert script',
    license     => 'Public Domain',
);

sub on_print_text {
  my ($dest, $text, $stripped) = @_;
  my $server = $dest->{server};

	my $sender = $stripped;
	$sender =~ s/^\<.([^\>]+)\>.+/\1/ ;
	return if (!($dest->{level} & MSGLEVEL_PUBLIC) || ($sender eq $server->{nick}));

	if(index($text,$server->{nick}) != -1) {
		system("play-audio /root/x/aka/alert.mp3");
	}
}

Irssi::signal_add('print text', 'on_print_text');
