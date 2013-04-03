#!/usr/bin/python
from os import system

# Groups:
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
	"misc.bib":      ["misc.bib", "nlin.AO.bib"]
}

for (k, v) in groups.iteritems():
    print 'Creating %s' % (k)
    for wildcard in v:
        print "\t", wildcard
        system("cat %s>>out/%s" % (wildcard, k))
