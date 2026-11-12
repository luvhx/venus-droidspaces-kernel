#!/bin/bash
# Compare exported-symbol CRCs between the DroidSpaces kernel and a baseline
# kernel built from the same source tree with the stock LineageOS config.
#
# The baseline is built with CONFIG_SYSVIPC/POSIX_MQUEUE off.  The kABI
# patches compile to their #else branch in that case, so the baseline has
# exactly the stock struct layout and the stock symbol CRCs.
set -e
W="$(cd "$(dirname "$0")/.." && pwd)"
STOCK="$W/out-stock/Module.symvers"
MOD="$W/out/Module.symvers"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

[ -f "$STOCK" ] || { echo "missing $STOCK (build out-stock first)" >&2; exit 2; }
[ -f "$MOD" ] || { echo "missing $MOD (build out first)" >&2; exit 2; }

norm() {
	awk -F'\t' '{
		c=tolower($1); sub(/^0x/,"",c); sub(/^0+/,"",c); if (c=="") c="0";
		if (!seen[$2]++) print $2"\t"c;
	}' "$1" | sort
}
norm "$STOCK" > "$TMP/stock"
norm "$MOD" > "$TMP/mod"

echo "stock exports: $(( $(wc -l < "$TMP/stock") ))"
echo "mod   exports: $(( $(wc -l < "$TMP/mod") ))"

awk -F'\t' '
	NR==FNR { k[$1]=$2; next }
	($1 in k) {
		common++;
		if (k[$1] != $2) {
			print "CRC MISMATCH " $1 " (stock=" k[$1] ", droidspaces=" $2 ")";
			bad++;
		}
		delete k[$1];
		next;
	}
	{ added++ }
	END {
		removed=0;
		for (s in k) removed++;
		printf "common: %d, crc mismatches: %d, added: %d, removed: %d\n",
		       common, bad+0, added, removed;
		for (s in k) print "REMOVED EXPORT " s;
		exit (bad || removed) ? 1 : 0;
	}
' "$TMP/stock" "$TMP/mod"

echo "kernel release: $(cat "$W/out/include/config/kernel.release")"
echo "stock release:  $(cat "$W/out-stock/include/config/kernel.release")"
