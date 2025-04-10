# template_db.py

INSTALLATION_METHODS = {
    "加装 - 粘贴": "Add on with double-sided tape or/and adhesive.",
    "加装 - 额外锁螺丝": "Bolt on or Screw on.",
    "加装 - 原车孔位锁螺丝": "Bolt on with OEM mounting points.",
    "加装 - 额外锁螺丝 + 打胶加固": "Bolt on or Screw on, secure with additional adhesive.",
    "加装 - 粘贴+原车孔位处锁螺丝": "Add on with OEM mounting points, Secure with additional screws or adhesive.",
    "替换 - 原车孔位处锁螺丝": "Replacement with OEM mounting points.",
    "替换 - 原车孔位处锁螺丝 + 额外螺丝加固卡扣位置": "Replacement with OEM mounting points, fasten clips with screws.",
    "替换 - 原车孔位处锁螺丝 + 额外打胶加固": "Replacement with OEM mounting points, secure with adhesive.",
    "加装 - 原车孔位锁螺丝 + 额外打胶/双面胶固定": "Bolt on with OEM mounting points, secure with additional adhesive.",
    "加装 - 粘贴 （无损安装）": "Add on with double-sided tape or/and adhesive.",
    "加装 - 额外螺丝": "Bolt on or Screw on.",
    "加装 - 原车孔位锁螺丝（无损安装）": "Bolt on with OEM mounting points.",
    "加装 - 额外螺丝+打胶/3M加固": "Bolt on or Screw on, secure with additional adhesive.",
    "加装 - 原车孔位锁螺丝+打胶/3M固定": "Add on with OEM mounting points, Secure with additional screws or adhesive.",
    "原车替换 (无损)": "Replacement with OEM mounting points.",
    "原车替换+卡扣位置螺丝加固": "Replacement with OEM mounting points, fasten clips with screws.",
    "原车替换+ 底部螺丝或打胶加固": "Replacement with OEM mounting points, secure with adhesive."
}

BUMPER_REMOVAL = {
    "是": "For best results, bumper removal recommended.",
    "否": "Bumper removal not needed."
}



MATERIAL_OPTIONS = {
    "碳纤-湿碳": {
        "variant": "Vacuumed Carbon",
        "description": "Real Vacuumed Carbon Fiber with UV Protection Clearcoat"
    },
    "碳纤-湿碳（半碳）": {
        "variant": "Partial Vacuumed Carbon",
        "description": "Partial Vacuumed Carbon Fiber with UV Protection Clearcoat: Combination of FRP and Carbon Fiber, FRP (Fiber Glass) is a composite material comprised of carbon fiber reinforced polymers. FRP Part comes with primed finish ready to be sanded and painted."
    },
    "碳纤-湿碳 （单面碳）机盖产品适用": {
        "variant": "Single-sided Vacuumed Carbon",
        "description": "-Top side: Carbon Fiber with UV Protection Clearcoat\n-Underside: FRP with Matte Black Primed Finish"
    },
    "碳纤-湿碳 （双面碳）机盖产品适用": {
        "variant": "Double-sided Vacuumed Carbon",
        "description": "-Top side: Carbon Fiber with UV Protection Clearcoat\n-Underside: Carbon Fiber with Matte Finish"
    },
    "碳纤-干碳": {
        "variant": "Pre-preg Carbon",
        "description": "Real Pre-preg (Dry) Carbon Fiber with UV Protection Clearcoat."
    },
    "碳纤-干碳（半碳）": {
        "variant": "Partial Pre-preg Carbon",
        "description": "Partial Pre-preg (Dry) Carbon Fiber with UV Protection Clearcoat: Combination of FRP and Carbon Fiber, FRP (Fiber Glass) is a composite material comprised of carbon fiber reinforced polymers. FRP Part comes with primed finish ready to be sanded and painted."
    },
    "碳纤-干碳 （单面碳）机盖产品适用": {
        "variant": "Single-sided Pre-preg Carbon",
        "description": "-Top side: Carbon Fiber with UV Protection Clearcoat\n-Underside: FRP with Matte Black Primed Finish"
    },
    "碳纤-干碳（双面碳）机盖产品适用": {
        "variant": "Double-sided Pre-preg Carbon",
        "description": "-Top side: Carbon Fiber with UV Protection Clearcoat\n-Underside: Carbon Fiber with Matte Finish"
    },
    "FRP": {
        "variant": "FRP or Carbon",
        "description": "FRP (Fiber Glass): a composite material comprised of carbon fiber reinforced polymers. FRP Part comes with primed finish ready to be sanded and painted."
    },
    "full frp": {
        "variant": "FRP or Carbon/Paintable",
        "description": "FRP or Carbon/Paintable - this product is meant to be painted by the end-user. The product may be made of FRP, partial carbon fiber, or carbon fiber. Customer does not get a choice between FRP or Carbon."
    },
    "碳纤 改 FRP": {
        "variant": "FRP or Carbon/Paintable",
        "description": "FRP or Carbon/Paintable - this product is meant to be painted by the end-user. The product may be made of FRP, partial carbon fiber, or carbon fiber. Customer does not get a choice between FRP or Carbon."
    },
    "ABS": {
        "variant": "ABS",
        "description": "ABS (Acrylonitrile Butadiene Styrene), is an opaque thermoplastic. It is an amorphous polymer comprised of three monomers, acrylonitrile, butadiene and styrene."
    },
    "PP": {
        "variant": "PP",
        "description": "Polypropylene (PP), also known as polypropene, is a thermoplastic polymer used in a wide variety of applications. It is produced via chain-growth polymerization from the monomer propylene."
    },
    "碳纤-干碳 (半成品)": {
        "variant": "Unpolished Carbon",
        "description": "Made of carbon fiber. Finished product is exposed carbon fiber. It is designed to be painted over during installation."
    },
    "铝": {
        "variant": "Aluminum",
        "description": "Aluminium or aluminum. It is designed to be painted over during installation."
    },
    "304不锈钢": {
        "variant": "Stainless steel",
        "description": ""
    },
    "钛合金": {
        "variant": "Titanium",
        "description": ""
    },
    "卡夫龙": {
        "variant": "Carbon Kevlar Hybrid",
        "description": "Carbon Kevlar Hybrid - a composite material that combines the high-strength properties of carbon fiber with the toughness and impact resistance of Kevlar. This hybrid material is used in applications that require both lightweight and durable performance, such as in aerospace, automotive, and sports equipment. The unique blend of carbon's rigidity and Kevlar's flexibility provides superior protection against wear, tear, and impact while maintaining strength and lightness."
    }
}


PATTERN_OPTIONS = {
    "卡夫龙": {
        "variant": "Carbon Kevlar Hybrid",
        "description": "Carbon Kevlar Hybrid with Color - Carbon Kevlar Hybrid that combines Carbon Fiber and Colored Kevlar. This material combines the strength of carbon fiber and the impact resistance of Kevlar, while adding vibrant, custom colors for aesthetic appeal. The blend of these materials, enhanced by the use of colored fibers or coatings, maintains exceptional durability and lightweight properties while offering a unique visual style. This hybrid material is commonly used in high-performance industries, where both appearance and functionality are key, such as in automotive, aerospace, and sports equipment."
    },
    "V纹": {
        "variant": "Woven 3K (V Shaped Weave)",
        "description": "V Shaped Weave - also known as book match weave. It is a type of fabric where the carbon fibers are interlaced in a distinct V-shaped pattern, providing enhanced strength and flexibility. This unique weaving technique helps distribute forces evenly across the material, making it particularly useful in high-performance applications like automotive and aerospace industries. The V-shape weave also offers improved durability and resistance to deformation, making it an ideal choice for components subjected to dynamic stresses."
    },
    "本田纹": {
        "variant": "Honda Black and Red Weave",
        "description": "Honda Black and Red Weave - carbon fiber weave that features a striking, dual-tone design that combines traditional carbon fiber with vibrant red accents for a unique aesthetic. This high-performance material maintains the strength, lightness, and durability of carbon fiber while adding a distinctive visual appeal, often seen in Honda's sports cars and racing models. The contrast between the red and black weave enhances both the functional and visual elements of the parts, making them stand out while offering superior strength and stiffness."
    },
    "斜纹14K": {
        "variant": "Woven 14K",
        "description": "Woven Carbon Fiber (14k) - consists of 14,000 individual carbon filaments bundled together in a single strand, offering a slightly lighter and more flexible alternative to higher filament counts. It is often used in applications where a balance between strength, weight, and cost is important, such as in the production of sporting goods, automotive parts, and lightweight structures. The 14k weave provides good durability and stiffness while maintaining a lower overall weight compared to heavier carbon fiber options."
    },
    "斜纹16K": {
        "variant": "Woven 16k",
        "description": "Woven Carbon Fiber (16k) - refers to the number of carbon filaments (16,000 fibers) bundled together in a single strand, offering a balance of strength and flexibility. This type of carbon fiber is commonly used in applications requiring high performance and durability, such as in automotive, aerospace, and sporting goods industries. The 16k weave provides a slightly thicker, more rigid structure compared to lower filament counts, making it suitable for parts that need to withstand substantial stress and load."
    },
    "斜纹3K": {
        "variant": "Woven 3k (default option)",
        "description": "Woven Carbon Fiber (Standard 2x2 or 3k) - the most common carbon fiber weave. 2x2 weave woven carbon fiber is the default if listing does not specify the pattern. Woven 3K carbon fiber is a lightweight and high-strength material made from bundles of 3,000 carbon filaments (referred to as \"3K\") that are woven into a fabric pattern, typically in a twill or plain weave. It offers excellent tensile strength, stiffness, and durability while maintaining a sleek, smooth appearance with a distinctive checkerboard pattern."
    },
    "锻造": {
        "variant": "Forged (20% extra charge, made to order)",
        "description": "Forged carbon fiber - a composite material made from randomly arranged, short carbon fiber strands combined with resin and compressed in a mold. Forged carbon fiber offers greater design flexibility compared to 3K woven carbon fiber, as it can be molded into more complex shapes without compromising structural integrity. Its random fiber orientation reduces weak points caused by the directional patterns in 3K weaves, enhancing impact resistance. Additionally, it has a unique aesthetic appeal, with a marbled texture that stands out from the uniform weave of 3K carbon fiber."
    },
    "蜂窝纹": {
        "variant": "Honeycomb (20% extra charge, made to order)",
        "description": "Honeycomb carbon fiber - combines woven 3K carbon fiber layers with a lightweight honeycomb weave, creating a sandwich structure that offers exceptional stiffness-to-weight ratio. This configuration provides excellent rigidity, impact resistance, and thermal insulation, making it ideal for aerospace, automotive, and high-performance sporting applications. The honeycomb weave significantly reduces material weight while maintaining strength, making it a preferred choice for lightweight structural components."
    }
}