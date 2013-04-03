#!/usr/bin/env python

from os import system
import glob

# Complete list of arXiv groups:
#    http://arxiv.org/archive/stat
#    http://arxiv.org/archive/math
#    http://arxiv.org/archive/physics
#    http://arxiv.org/archive/cond-mat
#    http://arxiv.org/corr/subjectclasses

groups = {
	"physics.bib":   ["physics.*.bib", "hep-*.bib", "nucl-th.bib", "gr-qc.bib", "cond-mat.*.bib"],
	"astro-ph.bib":  ["astro-ph.*.bib"],
	"quant.bib":     ["quant-ph.bib", "q-*.bib"],
	"math.bib":      ["math.*.bib"],
	"cs.bib":        ["cs.*.bib", "stat.*.bib"],
	"misc.bib":      ["nocat.bib", "nlin.AO.bib"]
}

for (k, v) in groups.iteritems():
    first  = False
    for wildcard in v:
        if len(glob.glob(wildcard)) >= 1:
            if not first:
                print 'Creating %s' % (k)
                first = True
                # Also create it, instead of appending to it.
                system("cat %s>%s" % (wildcard, k))
            else:
                system("cat %s>>%s" % (wildcard, k))
